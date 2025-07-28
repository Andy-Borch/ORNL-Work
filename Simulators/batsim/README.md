# Batsim Directory Overview

This repository contains results and scripts for evaluating the performance of various algorithms in Batsim.

- Subdirectories of simulation results organized by algorithm.
- Python scripts to generate synthetic workloads, run simulations, and visualize results.

## Directory Structure

```
.
├── results/
│   ├── conservative_bf_results/
│   ├── easy_bf_results/
│   └── ...
├── scripts/
│   ├── generate_workload.py
│   ├── compare_algorithms.py
│   ├── plot_results.py
│   └── ...
└── README.md
```

- `results/`: Contains subdirectories named after each algorithm, storing simulation output data.
- `scripts/`: Contains Python scripts for generating input workloads, executing simulations, and plotting performance results.

## Scripts Overview

### `generate_workload.py`
Generates synthetic workloads used as input for simulations.

### `compare_algorithms.py`
Compares performance metrics across different algorithms.

### `plot_results.py`
Generates plots and comparative graphs from simulation output files.

## Results

Simulation results are organized per algorithm. Each subdirectory may contain:
- Raw data files (e.g., `.csv`, `.json`)
- Logs and statistics
- Plots or figures summarizing performance metrics

## Dynamic Results (Work in Progress)

The current results and analyses are based on *static workloads*—that is, all jobs are known at the start of the simulation. We are looking into extending the framework to support *dynamic workloads*, where jobs arrive over time during simulation. This will allow for a more realistic evaluation of scheduling algorithms in online environments.

Future updates will include:
- Support for Batsim dynamic job submission
- Comparison of algorithm performance under dynamic conditions
