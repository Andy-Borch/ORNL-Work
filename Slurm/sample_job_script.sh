#!/bin/bash

JOB_ID=${SLURM_ARRAY_JOB_ID}
TASK_ID=${SLURM_ARRAY_TASK_ID}
NODE_NAME=$(hostname)

echo "Job Array ID: ${JOB_ID}. Task ID: ${TASK_ID}. Running on node: ${NODE_NAME}"

#Random sleep time to simulate a job running (real life this would be actual computation)
SLEEP_TIME=$((RANDOM % 11 + 5))
echo "Task ${TASK_ID} is sleeping for ${SLEEP_TIME} seconds."
sleep ${SLEEP_TIME}

echo "Task ${TASK_ID} completed on node ${NODE_NAME}."