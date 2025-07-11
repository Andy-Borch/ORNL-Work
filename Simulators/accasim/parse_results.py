import pandas as pd
import numpy as np
import os
import json
import re
from datetime import datetime

from accasim.base.scheduler_class import FirstInFirstOut as fifo_sched, ShortestJobFirst as sjf_sched, LongestJobFirst as ljf_sched, EASYBackfilling as easybf_sched
from accasim.base.allocator_class import FirstFit as ff_alloc, BestFit as bf_alloc
from accasim.experimentation.experiment import Experiment as experiment

# --- Helper function to extract UnixStartTime from SWF (needed for relative time) ---
def get_swf_unix_start_time(swf_filepath: str):
    unix_start_time = 0
    try:
        with open(swf_filepath, 'r') as f:
            for line in f:
                if line.startswith('; UnixStartTime:'):
                    unix_start_time = int(line.split(':')[1].strip())
                    break
    except:
        pass # Remain silent
    return unix_start_time

# --- Input SWF Parser (for the original workload, if needed for merging or config) ---
def parse_input_swf_trace(swf_filepath: str, system_max_procs: int = None):
    column_names = [
        "job_id", "submit_time_raw", "wait_time", "actual_runtime", "num_processors_used",
        "avg_cpu_used", "used_memory", "requested_num_processors", "requested_walltime",
        "status", "user_id", "group_id", "executable_num", "queue_id",
        "partition_id", "think_time", "something1", "something2"
    ]
    unix_start_time = None
    header_max_procs = None
    with open(swf_filepath, 'r') as f:
        for line in f:
            if line.startswith('; UnixStartTime:'):
                unix_start_time = int(line.split(':')[1].strip())
            elif line.startswith('; MaxProcs:'):
                header_max_procs = int(line.split(':')[1].strip())
            elif not line.startswith(';'):
                break
    if unix_start_time is None:
        unix_start_time = 0
    if system_max_procs is None and header_max_procs is not None:
        system_max_procs = header_max_procs
    elif system_max_procs is None:
        system_max_procs = 1000

    data_lines = []
    with open(swf_filepath, 'r') as f:
        for line in f:
            if not line.startswith(';'):
                processed_line = line.replace('.00', '').strip()
                parts = processed_line.split()
                if len(parts) == len(column_names):
                    data_lines.append(parts)

    df = pd.DataFrame(data_lines, columns=column_names)
    for col in ["job_id", "submit_time_raw", "actual_runtime",
                "num_processors_used", "requested_num_processors",
                "requested_walltime"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=["job_id", "submit_time_raw", "actual_runtime",
                        "requested_num_processors", "requested_walltime"], inplace=True)
    df['job_id'] = df['job_id'].astype(int)
    df['submit_time'] = df['submit_time_raw'] - df['submit_time_raw'].min()

    df['num_processors'] = df['requested_num_processors'].replace(-1, system_max_procs)
    df['num_processors'] = df['num_processors'].clip(lower=1, upper=system_max_procs)
    default_large_walltime = 3600 * 1000
    df['requested_walltime'] = df['requested_walltime'].replace(-1, default_large_walltime)
    df['requested_walltime'] = df.apply(
        lambda row: max(row['requested_walltime'], row['actual_runtime']) if row['requested_walltime'] < row['actual_runtime'] else row['requested_walltime'],
        axis=1
    )
    df['requested_walltime'] = df['requested_walltime'].clip(lower=1)
    final_df = df[[
        "job_id", "submit_time", "num_processors", "requested_walltime", "actual_runtime"
    ]].copy()
    final_df['submit_time'] = final_df['submit_time'].astype(int)
    final_df['num_processors'] = final_df['num_processors'].astype(int)
    final_df['requested_walltime'] = final_df['requested_walltime'].astype(int)
    final_df['actual_runtime'] = final_df['actual_runtime'].astype(int)
    return final_df

# --- Parser for 'sched-system-workload.swf' ---
def parse_accasim_schedule_output(filepath: str):
    try:
        df = pd.read_csv(filepath, sep='\n', header=None, names=['full_line'], comment='#')
    except pd.errors.EmptyDataError:
        return pd.DataFrame()
    except:
        return pd.DataFrame()

    split_data = df['full_line'].str.split(';', expand=True)

    primary_column_names = [
        "job_id", "user_id", "queue_assign_start_time_compound", "end_time_str",
        "total_nodes_requested", "total_cpu_requested", "total_mem_requested", "expected_duration",
        "trailing_empty_col"
    ]

    if split_data.shape[1] > len(primary_column_names):
        split_data.columns = primary_column_names + [f'extra_col_{i}' for i in range(split_data.shape[1] - len(primary_column_names))]
    elif split_data.shape[1] < len(primary_column_names):
        temp_df = pd.DataFrame(columns=primary_column_names)
        for col_idx, col_name in enumerate(primary_column_names):
            if col_idx < split_data.shape[1]:
                temp_df[col_name] = split_data.iloc[:, col_idx]
        split_data = temp_df.copy()
    else:
        split_data.columns = primary_column_names

    if 'trailing_empty_col' in split_data.columns:
        if split_data['trailing_empty_col'].isnull().all():
            split_data = split_data.drop(columns=['trailing_empty_col'])

    compound_regex = r"^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})__((?:.|\n)*)__(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})$"

    parsed_compound = split_data['queue_assign_start_time_compound'].astype(str).str.extract(compound_regex)
    if not parsed_compound.empty and parsed_compound.shape[1] == 3:
        split_data[['queue_time_raw_str', 'assigned_nodes_raw_str', 'start_time_raw_str']] = parsed_compound
    else:
        split_compound_fallback = split_data['queue_assign_start_time_compound'].astype(str).apply(
            lambda x: (x.split('__', 1)[0] if '__' in x else x,
                        x.split('__')[-1] if '__' in x else np.nan,
                        x.split('__', 1)[1].rsplit('__', 1)[0] if x.count('__') > 1 else np.nan)
        ).tolist()
        split_data[['queue_time_raw_str', 'start_time_raw_str', 'assigned_nodes_raw_str']] = pd.DataFrame(split_compound_fallback, index=split_data.index)


    split_data['queue_time_dt'] = pd.to_datetime(split_data['queue_time_raw_str'], errors='coerce')
    split_data['start_time_dt'] = pd.to_datetime(split_data['start_time_raw_str'], errors='coerce')
    split_data['end_time_dt'] = pd.to_datetime(split_data['end_time_str'], errors='coerce')

    min_sim_time_epoch = split_data['start_time_dt'].min()
    if pd.isna(min_sim_time_epoch):
        min_sim_time_epoch = split_data['queue_time_dt'].min()
    if pd.isna(min_sim_time_epoch):
        min_sim_time_epoch = datetime(1970, 1, 1)

    split_data['submit_time'] = (split_data['queue_time_dt'] - min_sim_time_epoch).dt.total_seconds().fillna(0).astype(int).clip(lower=0)
    split_data['start_time'] = (split_data['start_time_dt'] - min_sim_time_epoch).dt.total_seconds().fillna(0).astype(int).clip(lower=0)
    split_data['end_time'] = (split_data['end_time_dt'] - min_sim_time_epoch).dt.total_seconds().fillna(0).astype(int).clip(lower=0)

    numeric_cols = ["job_id", "user_id", "total_nodes_requested", "total_cpu_requested", "total_mem_requested", "expected_duration"]
    for col in numeric_cols:
        if col in split_data.columns:
            split_data[col] = pd.to_numeric(split_data[col], errors='coerce').fillna(-1).astype(int)

    split_data['actual_runtime'] = split_data['end_time'] - split_data['start_time']
    split_data['wait_time'] = split_data['start_time'] - split_data['submit_time']
    split_data['turnaround_time'] = split_data['end_time'] - split_data['submit_time']

    split_data['slowdown'] = split_data.apply(
        lambda row: (row['wait_time'] + row['actual_runtime']) / row['actual_runtime'] if row['actual_runtime'] > 0 else float('inf'),
        axis=1
    )
    split_data['slowdown'] = split_data['slowdown'].replace([np.inf, -np.inf], np.nan).clip(upper=1000)

    split_data['status'] = np.where(split_data['actual_runtime'] > 0, 1, 0)

    final_cols = [
        "job_id", "submit_time", "start_time", "end_time", "actual_runtime",
        "requested_walltime", "requested_num_processors", "num_processors_allocated",
        "wait_time", "turnaround_time", "slowdown", "status", "user_id",
        "requested_nodes",
        "requested_memory"
    ]
    split_data['requested_num_processors'] = split_data['total_cpu_requested']
    split_data['num_processors_allocated'] = split_data['total_cpu_requested']
    split_data['requested_nodes'] = split_data['total_nodes_requested']
    split_data['requested_memory'] = split_data['total_mem_requested']

    for col in final_cols:
        if col not in split_data.columns:
            split_data[col] = np.nan

    return split_data[final_cols]

# --- Parser for 'bench-system-workload.swf' ---
def parse_accasim_benchmark_output(filepath: str):
    column_names = [
        "timestamp_absolute",
        "event_status",
        "metric_value_1",
        "metric_value_2",
        "metric_value_3",
        "resource_usage_value"
    ]
    try:
        df = pd.read_csv(filepath, sep=';', header=None, names=column_names, comment='#', skipinitialspace=True)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()
    except:
        return pd.DataFrame()

    for col in column_names:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(inplace=True)

    if not df.empty and 'timestamp_absolute' in df.columns:
        min_timestamp = df['timestamp_absolute'].min()
        df['time_relative_seconds'] = df['timestamp_absolute'] - min_timestamp
        df['time_relative_seconds'] = df['time_relative_seconds'].astype(int).clip(lower=0)
    else:
        df['time_relative_seconds'] = 0

    df.rename(columns={
        "timestamp_absolute": "benchmark_absolute_timestamp",
        "event_status": "benchmark_event_status",
        "metric_value_1": "benchmark_metric_1_time",
        "metric_value_2": "benchmark_metric_2_ratio",
        "metric_value_3": "benchmark_metric_3_rate",
        "resource_usage_value": "benchmark_resource_load_procs"
    }, inplace=True)
    
    final_bench_cols = [
        "time_relative_seconds", "benchmark_resource_load_procs",
        "benchmark_metric_1_time", "benchmark_metric_2_ratio", "benchmark_metric_3_rate",
        "benchmark_event_status", "benchmark_absolute_timestamp"
    ]
    
    for col in final_bench_cols:
        if col not in df.columns:
            df[col] = np.nan

    return df[final_bench_cols]

# --- Main Execution Block ---
if __name__ == '__main__':
    experiment_name = 'Demo_Experiment'
    
    workload_path = '/home/er3/ORNL-Work/Simulators/accasim/workloads/system-workload.swf'
    sys_config_path = '/home/er3/ORNL-Work/Simulators/accasim/config/HPC2N.config'    
    essentials_path = '/home/er3/ORNL-Work/Simulators/accasim/config/essentials.config'

    unix_start_time_from_swf = get_swf_unix_start_time(workload_path)

    total_system_processors = 0
    try:
        with open(sys_config_path, 'r') as f:
            sys_config_data = json.load(f)
            if 'nodes' in sys_config_data and isinstance(sys_config_data['nodes'], list):
                for node_group in sys_config_data['nodes']:
                    if 'count' in node_group and 'properties' in node_group and 'core' in node_group['properties']:
                        total_system_processors += node_group['count'] * node_group['properties']['core']
            elif 'properties' in sys_config_data and 'core' in sys_config_data['properties']:
                if 'num_nodes' in sys_config_data:
                     total_system_processors = sys_config_data['num_nodes'] * sys_config_data['properties']['core']
                elif 'node_count' in sys_config_data:
                    total_system_processors = sys_config_data['node_count'] * sys_config_data['properties']['core']
    except:
        pass # Remain silent
    
    if total_system_processors == 0:
        total_system_processors = 240 # Fallback default

    sched_list = [fifo_sched, sjf_sched, ljf_sched, easybf_sched]
    alloc_list = [ff_alloc, bf_alloc]

    experimentation = experiment(
        experiment_name, 
        workload_path, 
        sys_config_path, 
        simulator_config=essentials_path, 
        SEPARATOR='#', 
        timeout=3600
    )
    
    experimentation.generate_dispatchers(sched_list, alloc_list)
    experimentation.run_simulation(generate_plot=False) 

    all_job_stats_dataframes = []
    all_bench_stats_dataframes = []

    base_output_dir = os.path.join(os.getcwd(), experiment_name) 
    
    for sched_class in sched_list: 
        for alloc_class in alloc_list:
            scheduler_name = sched_class.__name__
            allocator_name = alloc_class.__name__
            
            run_folder = os.path.join(base_output_dir, f"{scheduler_name}{experimentation.separator_char}{allocator_name}")
            
            schedule_output_filename = f"sched-{os.path.basename(workload_path)}"
            schedule_full_path = os.path.join(run_folder, schedule_output_filename) 

            if os.path.exists(schedule_full_path):
                try:
                    job_df = parse_accasim_schedule_output(schedule_full_path)
                    if not job_df.empty:
                        job_df['scheduler'] = scheduler_name
                        job_df['allocator'] = allocator_name
                        all_job_stats_dataframes.append(job_df)
                except:
                    pass # Remain silent

            benchmark_output_filename = f"bench-{os.path.basename(workload_path)}"
            benchmark_full_path = os.path.join(run_folder, benchmark_output_filename)

            if os.path.exists(benchmark_full_path):
                try:
                    bench_df = parse_accasim_benchmark_output(benchmark_full_path)
                    if not bench_df.empty:
                        bench_df['scheduler'] = scheduler_name
                        bench_df['allocator'] = allocator_name
                        all_bench_stats_dataframes.append(bench_df)
                except:
                    pass # Remain silent

    if all_job_stats_dataframes:
        final_job_stats_df = pd.concat(all_job_stats_dataframes, ignore_index=True)
        job_stats_csv_path = os.path.join(experiment_name, f"{experiment_name}_job_stats.csv")
        final_job_stats_df.to_csv(job_stats_csv_path, index=False)

    if all_bench_stats_dataframes:
        final_bench_stats_df = pd.concat(all_bench_stats_dataframes, ignore_index=True)
        bench_stats_csv_path = os.path.join(experiment_name, f"{experiment_name}_benchmark_stats.csv")
        final_bench_stats_df.to_csv(bench_stats_csv_path, index=False)