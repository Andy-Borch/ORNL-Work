#from batsim.pybatsim_test import Batsim, BatsimJob, BatsimProfile, BatsimEvent, BatsimScheduler, batsim_main
#from pybatsim_test import BatsimScheduler, batsim_main
from pybatsim import Batsim

import argparse
import random
from collections import deque

# QoS levels and priorities
QOS_PRIORITY = {'high': 3, 'medium': 2, 'low': 1}
AGING_THRESHOLD = 100
FAILURE_PROBABILITY = 0.1

class QoSPreemptiveScheduler(BatsimScheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queues = {'high': deque(), 'medium': deque(), 'low': deque()}
        self.job_arrival_times = {}

    def onAfterBatsimInit(self):
        print("Scheduler initialized.")

    def onJobSubmission(self, job):
        qos = job.metadata.get("qos", "low")
        self.queues[qos].append(job)
        self.job_arrival_times[job.id] = self.now()
        print(f"[{self.now()}] Job {job.id} submitted with QoS '{qos}'.")

    def onJobCompletion(self, job):
        print(f"[{self.now()}] Job {job.id} completed.")

    def onJobFailure(self, job):
        print(f"[{self.now()}] Job {job.id} FAILED.")

    def preempt_lower_priority_jobs(self, needed_res, min_priority):
        preempted = []
        for running_job in self.running_jobs:
            job_qos = running_job.metadata.get("qos", "low")
            if QOS_PRIORITY[job_qos] < min_priority:
                self.kill_job(running_job)
                preempted.append(running_job)
                needed_res -= running_job.required_resources
                if needed_res <= 0:
                    break
        return needed_res <= 0

    def age_jobs(self):
        now = self.now()
        for level in ['low', 'medium']:
            next_level = 'medium' if level == 'low' else 'high'
            for job in list(self.queues[level]):
                if now - self.job_arrival_times[job.id] > AGING_THRESHOLD:
                    print(f"[{now}] Aging: Promoting job {job.id} from {level} to {next_level}")
                    self.queues[level].remove(job)
                    self.queues[next_level].append(job)

    def maybe_fail_job(self, job):
        if random.random() < FAILURE_PROBABILITY:
            self.fail_job(job)
            print(f"[{self.now()}] Simulated failure of job {job.id}")
            return True
        return False

    def schedule(self):
        self.age_jobs()
        available = self.get_available_resources()

        for qos_level in ['high', 'medium', 'low']:
            for job in list(self.queues[qos_level]):
                if job.required_resources <= len(available):
                    if self.maybe_fail_job(job):
                        self.queues[qos_level].remove(job)
                        continue
                    self.execute_job(job, available[:job.required_resources])
                    available = available[job.required_resources:]
                    self.queues[qos_level].remove(job)
                elif qos_level == 'high':
                    if self.preempt_lower_priority_jobs(job.required_resources, QOS_PRIORITY[qos_level]):
                        print(f"[{self.now()}] Preempted jobs to make room for high-priority job {job.id}")
                        return  # Wait until preempted jobs are actually stopped

# 🔧 Main CLI handler
def main():
    parser = argparse.ArgumentParser(description="QoS Preemptive Batsim Scheduler")
    parser.add_argument('--socket', type=str, default='localhost', help='Batsim socket address')
    parser.add_argument('--port', type=int, default=28000, help='Batsim port')
    args = parser.parse_args()

    print(f"Connecting to Batsim at {args.socket}:{args.port}")
    batsim_main(QoSPreemptiveScheduler, address=args.socket, port=args.port)

if __name__ == '__main__':
    main()
