# Tools and Analysis for HPC Job Scheduling Research

This repository contains code developed during a summer internship at **Oak Ridge National Laboratory (ORNL)** to support research into **job scheduling and submission data and ineractive/urgent mechanisms** on HPC systems like **Frontier**.

The repository is organized into two main components:

- [`Workflow/`](./Workflow): Scripts for processing and visualizing HPC job submission data.
- [`Simulators/`](./Simulators): Code for evaluating existing job scheduler simulators for support of advanced scheduling features.

---

##  Related Publications

The work in the `Workflow/` directory contributed to a research paper that has been accepted to the following conference:

**Title:** _"An LLM-Enabled Workflow for Understanding and Evolving HPC Job Scheduling Practices"_  
**Conference:** 1st Workshop on Workflows, Intelligent Scientific Data, and Optimization for Automated Management, ICPP 2025

The work in the `Simulator/` directory contributed to a research paper that has been accepted to the following conference:

**Title:** _"Evaluating HPC Scheduling Strategies for Urgent Workloads"_  
**Conference:** Sixth Combined Workshop on Interactive and Urgent High-Performance Computing, SC25

While the paper is not yet published, this repository reflects some of the core techniques and visual outputs described in the work.

---

##  Workflow Directory

The `Workflow/` directory includes code that:

- Parses CSV files from prior workflow stages
- Generates visualizations to explore:
  - Job durations
  - Queue/wait times
  - Node usage
  - Job state distributions
  - Backfilling behavior
- Creates a user freindly dashboard with results

### Context

This work is part of a workflow that processes job scheduler logs and outputs visual insights. These insights help HPC researchers and system administrators understand scheduling trends and resource utilization on systems such as ORNL's **Frontier** supercomputer.

### Full Workflow Diagram

![Full workflow](https://github.com/Andy-Borch/ORNL-Work/blob/main/Dashboard/assets/actual_workflow.png)

> This repository corresponds to the **data visualization** stage of the above pipeline.

---

##  Simulators Directory

The `Simulators/` directory explores the capabilities of various existing HPC job scheduler simulators. The goal is to evaluate:

- Whether simulators support **user-level QoS (Quality of Service)** configurations
- If they allow **urgent or high-priority job submissions**
- How flexible they are for further research

Each simulator is tested and analyzed for these features. Results are documented in the respective subdirectories.

---
