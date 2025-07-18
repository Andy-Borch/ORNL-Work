import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from evalys.jobset import JobSet
from evalys import visu
import evalys.visu.gantt # Already using this
import pandas as pd # Good to have for data manipulation
import numpy as np # Often useful for calculations
# Load your JobSet
js = JobSet.from_csv("/home/er3/ORNL-Work/Simulators/batsim/out_jobs.csv")
# --- Data Preparation (Run once for all plots) ---

# Define the correct column names based on your provided list
SUBMISSION_TIME_COL = 'submission_time'
START_TIME_COL = 'starting_time' # Corrected name
FINISH_TIME_COL = 'finish_time'
ALLOCATED_RESOURCES_STR_COL = 'allocated_resources' # This seems to be the list of resources
# You don't have a 'ret' column in your list, so let's adjust for 'success' or 'final_state'

# --- Handle job success/failure ---
# Based on your column list, 'success' (boolean) or 'final_state' (string like 'COMPLETED', 'FAILED')
# would be used instead of 'ret'. Let's use 'success' if available, otherwise 'final_state'.
success_failure_col = None
if 'success' in js.df.columns:
    success_failure_col = 'success'
elif 'final_state' in js.df.columns:
    success_failure_col = 'final_state'
else:
    print("Warning: Neither 'success' nor 'final_state' column found for failure analysis.")

if success_failure_col:
    # Ensure success/final_state column is appropriate
    if success_failure_col == 'success':
        # 'success' is likely boolean (True for success, False for failure)
        js.df['is_failed'] = ~js.df['success'].astype(bool) # Convert to boolean and invert
    elif success_failure_col == 'final_state':
        # 'final_state' is likely a string like 'COMPLETED', 'FAILED', 'REJECTED', etc.
        # We'll consider anything not 'COMPLETED' as a failure for the histogram,
        # but you might want to refine this (e.g., only 'FAILED' states).
        js.df['is_failed'] = (js.df['final_state'] != 'COMPLETED') & pd.notnull(js.df['final_state'])
else:
    js.df['is_failed'] = False # Default to no failures if no info

# --- Calculate 'allocated_resources_count' ---
# The 'allocated_resources' column appears to be a string representation of a list (e.g., "[0,1,2]")
# We need to parse this to get the count of allocated resources for utilization.
if ALLOCATED_RESOURCES_STR_COL in js.df.columns:
    # Safely evaluate the string list into an actual list and get its length
    # Handle NaN or empty strings gracefully
    js.df['allocated_resources_count'] = js.df[ALLOCATED_RESOURCES_STR_COL].apply(
        lambda x: len(eval(x)) if pd.notnull(x) and isinstance(x, str) and x.strip() else 0
    )
    # If the column might contain non-string representations of list (e.g., already parsed lists or None),
    # a more robust check might be needed:
    # js.df['allocated_resources_count'] = js.df[ALLOCATED_RESOURCES_STR_COL].apply(
    #     lambda x: len(x) if isinstance(x, list) else (len(eval(x)) if pd.notnull(x) and isinstance(x, str) and x.strip() else 0)
    # )
else:
    print(f"Warning: '{ALLOCATED_RESOURCES_STR_COL}' column not found. Cannot calculate resource utilization based on allocated resources.")
    print("Falling back to 'requested_number_of_resources' for utilization estimates, but this may be inaccurate.")
    # Fallback to requested_number_of_resources if allocated_resources is missing
    js.df['allocated_resources_count'] = js.df['requested_number_of_resources'].apply(lambda x: x if pd.notnull(x) else 1)


# Convert relevant time columns to numeric, handling potential non-numeric values
time_cols_to_convert = [SUBMISSION_TIME_COL, START_TIME_COL, FINISH_TIME_COL]
for col in time_cols_to_convert:
    if col in js.df.columns: # Check if column exists before converting
        js.df[col] = pd.to_numeric(js.df[col], errors='coerce')
    else:
        print(f"Warning: Time column '{col}' not found in DataFrame. Some plots may be affected.")


# --- Initial Data Exploration (Output to File) ---
output_filename = "./jobset_description.txt"
print(f"--- Writing JobSet DataFrame Description and Columns to {output_filename} ---")
with open(output_filename, 'w') as f:
    f.write("--- JobSet DataFrame Description ---\n")
    f.write(js.df.describe().to_string()) # Use to_string() for full DataFrame representation
    f.write("\n\n")
    f.write("Columns in js.df:\n")
    f.write(str(js.df.columns.tolist())) # Convert list to string for writing
    f.write("\n")

# --- Gantt Chart ---
print("\n--- Generating Gantt Chart ---")
# Evalys's gantt function typically uses 'start_time' and 'finish_time' internally.
# It might automatically map your 'starting_time' to its internal 'start_time'.
# If it fails here, the Evalys version might not handle custom column names automatically.
try:
    visu.gantt.plot_gantt(js)
    plt.title('Gantt Chart of Job Schedule')
    plt.savefig("./gantt_chart.png", dpi=300, bbox_inches='tight')
    plt.show()
except Exception as e:
    print(f"Warning: Gantt chart generation failed: {e}")
    print("Evalys's gantt function might expect specific column names (e.g., 'start_time', 'finish_time').")
    print("If it's critical, consider manually renaming columns or using a custom gantt plot.")


# --- Job Failure Histogram ---
print("\n--- Generating Job Failure Histogram ---")
if 'is_failed' in js.df.columns:
    # Filter for jobs that are marked as failed
    failed_jobs_df = js.df[js.df['is_failed']].copy()

    if not failed_jobs_df.empty:
        # For a histogram of failures, we need a categorical variable to count.
        # If using 'final_state', we can count states like 'FAILED', 'REJECTED'.
        # If using 'success', we just count 'False' (failures).

        if success_failure_col == 'final_state':
            # Count different non-completed final states
            failure_counts = failed_jobs_df['final_state'].value_counts().sort_index()
            x_label = 'Final State (Non-COMPLETED)'
        else: # Likely using 'success' or just a generic failure count
            # A simple count of True in 'is_failed' is already available.
            # For a histogram, we could just say "Failed" vs "Not Failed"
            # Or count distinct return codes if you had them.
            # Since you don't have 'ret', a bar plot of final_state or just total failures is best.
            # Let's count occurrences of 'success' == False or just show total
            failure_counts = pd.Series({'Failed Jobs': len(failed_jobs_df)})
            x_label = 'Failure Type'

        plt.figure(figsize=(10, 6))
        failure_counts.plot(kind='bar')
        plt.title('Distribution of Job Failures')
        plt.xlabel(x_label)
        plt.ylabel('Number of Jobs')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("./job_failure_histogram.png", dpi=300)
        plt.show()

        print(f"Total failed jobs: {len(failed_jobs_df)}")
        if success_failure_col == 'final_state':
            print("Failure counts by final state:\n", failure_counts)
        elif success_failure_col == 'success':
            print("Number of jobs where 'success' is False (failures):", len(failed_jobs_df))

    else:
        print("No job failures found in the dataset (all jobs 'success' or 'COMPLETED').")
else:
    print("Skipping job failure histogram: No 'success' or 'final_state' column found.")


# --- Queue Length Over Time (Line Chart) ---
print("\n--- Generating Queue Length Over Time Chart ---")
if START_TIME_COL in js.df.columns and SUBMISSION_TIME_COL in js.df.columns:
    events = []
    for index, job in js.df.iterrows():
        if pd.notnull(job[SUBMISSION_TIME_COL]): events.append((job[SUBMISSION_TIME_COL], 'submit'))
        if pd.notnull(job[START_TIME_COL]): events.append((job[START_TIME_COL], 'start'))
    events.sort(key=lambda x: x[0])

    time_points_queue = []
    queue_lengths = []
    current_queue_length = 0

    for time, event_type in events:
        if not time_points_queue or time > time_points_queue[-1]:
            time_points_queue.append(time)
            queue_lengths.append(current_queue_length)
        if event_type == 'submit': current_queue_length += 1
        elif event_type == 'start': current_queue_length = max(0, current_queue_length - 1)
        time_points_queue.append(time)
        queue_lengths.append(current_queue_length)

    if time_points_queue: # Ensure there's data to plot
        plt.figure(figsize=(14, 7))
        plt.step(time_points_queue, queue_lengths, where='post', label='Jobs in Queue')
        plt.title('Queue Length Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Number of Jobs in Queue')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.savefig("./queue_length_over_time.png", dpi=300)
        plt.show()
    else:
        print("No valid events found to plot queue length.")
else:
    print("Skipping Queue Length plot due to missing submission or starting time columns.")


# --- Total Resource Utilization Over Time (Line Chart) ---
print("\n--- Generating Total Resource Utilization Over Time Chart ---")
if START_TIME_COL in js.df.columns and FINISH_TIME_COL in js.df.columns and 'allocated_resources_count' in js.df.columns:
    events = []
    for index, job in js.df.iterrows():
        if pd.notnull(job[START_TIME_COL]) and pd.notnull(job[FINISH_TIME_COL]) and pd.notnull(job['allocated_resources_count']):
            resources = job['allocated_resources_count']
            events.append((job[START_TIME_COL], resources, 'start'))
            events.append((job[FINISH_TIME_COL], resources, 'end'))
    events.sort(key=lambda x: x[0])

    current_utilization = 0
    utilization_data = []

    if events:
        utilization_data.append((events[0][0], 0)) # Initialize at first event time
        for time, resources, event_type in events:
            if utilization_data[-1][0] < time:
                utilization_data.append((time, current_utilization))
            if event_type == 'start': current_utilization += resources
            elif event_type == 'end': current_utilization = max(0, current_utilization - resources)
            utilization_data.append((time, current_utilization))

        times, utilizations = zip(*utilization_data)
        plt.figure(figsize=(14, 7))
        plt.step(times, utilizations, where='post')
        plt.title('Total CPU Utilization Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Number of CPUs Utilized')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("./total_cpu_utilization_over_time.png", dpi=300)
        plt.show()
    else:
        print("No valid job start/finish events found to plot resource utilization.")
else:
    print("Skipping Total Resource Utilization plot due to missing starting/finish time or allocated resources count columns.")

print("\n--- All requested plots generated. ---")