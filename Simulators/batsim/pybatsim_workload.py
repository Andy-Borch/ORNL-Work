import argparse
import json
import random

QOS_LEVELS = ['low', 'medium', 'high']
DEFAULT_PROFILE = "default"

def generate_workload(num_jobs, urgent_percent, fail_percent, output_file):
    jobs = []

    for i in range(num_jobs):
        job_id = f"job_{i}"
        subtime = random.randint(0, 500)
        res = random.randint(1, 4)
        walltime = random.randint(50, 300)

        # Assign QoS
        if random.random() < (urgent_percent / 100):
            qos = "high"
        else:
            qos = random.choices(QOS_LEVELS, weights=[0.6, 0.3, 0.1])[0]  # more low/med jobs

        # Simulate failure tag
        will_fail = random.random() < (fail_percent / 100)

        job = {
            "id": job_id,
            "subtime": subtime,
            "res": res,
            "walltime": walltime,
            "profile": DEFAULT_PROFILE,
            "metadata": {
                "qos": qos
            }
        }

        if will_fail:
            job["metadata"]["will_fail"] = True  # used optionally by scheduler

        jobs.append(job)

    workload = {
        "version": "2.0",
        "jobs": jobs
    }

    with open(output_file, 'w') as f:
        json.dump(workload, f, indent=2)

    print(f"✅ Generated {num_jobs} jobs into '{output_file}'")
    print(f"   QoS: ~{urgent_percent}% urgent/high")
    print(f"   Failures: ~{fail_percent}% tagged as 'will_fail'")

# 🔧 CLI Entry
def main():
    parser = argparse.ArgumentParser(description="Generate synthetic Batsim workload")
    parser.add_argument('--jobs', type=int, required=True, help="Total number of jobs to generate")
    parser.add_argument('--urgent-percent', type=float, default=10.0, help="Percentage of urgent (high-QoS) jobs")
    parser.add_argument('--fail-percent', type=float, default=5.0, help="Percentage of jobs marked to fail")
    parser.add_argument('--output', type=str, default='workload.json', help="Output file name")
    args = parser.parse_args()

    generate_workload(
        num_jobs=args.jobs,
        urgent_percent=args.urgent_percent,
        fail_percent=args.fail_percent,
        output_file=args.output
    )

if __name__ == '__main__':
    main()
