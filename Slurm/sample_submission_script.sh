#!/bin/bash

#SBATCH --job-name=my_array_jobs    # Job name
#SBATCH --output=slurm-%A_%a.out    # Standard output and error log
#SBATCH --error=slurm-%A_%a.err     # Error log
#SBATCH --ntasks=1                  # Single task per job entry
#SBATCH --cpus-per-task=1           # Single CPU per task
#SBATCH --array=0-9%10              # Create 10 jobs (0-9), run max 10 concurrently
#SBATCH --time=0-00:02:00           # Max wall time (2 minutes)
#SBATCH --mem-per-cpu=100M          # Memory per CPU

echo "Submitting job array with 10 tasks."
echo "Each task will request 1 CPU."
echo "Maximum 10 tasks will run concurrently."

#Can br any program or script, here we use the sample job script
./sample_job_script.sh
echo "Job array submitted. Check the output files for each task."

