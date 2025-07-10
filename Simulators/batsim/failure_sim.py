import json
import random
import argparse
import os

def simulate_failures(
    input_workload_path: str,
    output_workload_path: str,
    job_failure_rate_range: tuple[float, float],
    critical_failure_rate_range: tuple[float, float]
):
    """
    Simulates random job failures and 'critical' job failures (potentially indicating node issues)
    in a Batsim workload JSON file by modifying the job profiles.

    Args:
        input_workload_path: Path to the original Batsim workload JSON file.
        output_workload_path: Path to save the modified workload JSON file.
        job_failure_rate_range: A tuple (min_percent, max_percent) for the
                                percentage of jobs that will experience a general failure.
                                (e.g., (3.0, 15.0) for 3-15%)
        critical_failure_rate_range: A tuple (min_percent, max_percent) for the
                                     percentage of *failed* jobs that will be marked as
                                    'critical' (e.g., return_code=99), potentially
                                    simulating a node-related issue. This is a percentage
                                     *of the jobs that have already failed*.
    """
    if not os.path.exists(input_workload_path):
        print(f"Error: Input workload file not found at '{input_workload_path}'")
        return

    try:
        with open(input_workload_path, 'r') as f:
            workload = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Could not parse JSON from '{input_workload_path}'. Please ensure it's valid JSON. Error: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the input file: {e}")
        return

    jobs = workload.get('jobs', [])
    profiles = workload.get('profiles', {})
    
    if not jobs:
        print("Warning: No 'jobs' array found or it is empty in the input workload file. No modifications were made.")
        return

    # Validate percentage ranges
    if (job_failure_rate_range[0] < 0 or job_failure_rate_range[1] > 100):
        print(f"Error: Invalid job failure rate range: {job_failure_rate_range}. Values must be between 0 and 100.")
        return
    if (critical_failure_rate_range[0] < 0 or critical_failure_rate_range[1] > 100):
        print(f"Error: Invalid critical failure rate range: {critical_failure_rate_range}. Values must be between 0 and 100.")
        return

    # Determine the actual failure percentages for this run
    job_failure_rate = random.uniform(job_failure_rate_range[0], job_failure_rate_range[1]) / 100.0
    critical_failure_rate = random.uniform(critical_failure_rate_range[0], critical_failure_rate_range[1]) / 100.0

    num_jobs = len(jobs)
    num_jobs_to_fail = int(num_jobs * job_failure_rate)
    
    if num_jobs_to_fail > num_jobs:
        num_jobs_to_fail = num_jobs
        print(f"Warning: Calculated jobs to fail ({int(job_failure_rate * 100)}%) exceeds total jobs. Failing all jobs.")

    failed_job_indices = random.sample(range(num_jobs), num_jobs_to_fail)

    num_general_failures = 0
    num_critical_failures = 0
    
    # Dictionary to store new profiles created for failures
    # Key: (original_profile_name, failure_return_code) -> Value: new_profile_name
    failed_profile_map = {} 

    for i, job in enumerate(jobs):
        original_profile_name = job.get('profile')
        if not original_profile_name:
            print(f"Warning: Job {job.get('id', i)} has no 'profile' field. Skipping failure simulation for this job.")
            continue # Cannot simulate failure if no profile to modify

        # Remove any existing failure_type metadata to ensure a clean slate
        if 'metadata' in job and 'failure_type' in job['metadata']:
            del job['metadata']['failure_type']

        if i in failed_job_indices:
            # This job is marked for failure
            
            # Determine the return code for this specific job's profile
            profile_return_code = 1 # Default general failure

            # Check if this failure is 'critical' (node-related)
            if random.random() < critical_failure_rate:
                profile_return_code = 99 # Special code for critical/node-related failure
                # Add metadata for potential scheduler interpretation
                if 'metadata' not in job:
                    job['metadata'] = {}
                job['metadata']['failure_type'] = 'node_induced'
                num_critical_failures += 1
            else:
                num_general_failures += 1

            # Create a new profile for this failing job if it doesn't exist
            # This ensures that only selected jobs fail, even if profiles are shared
            new_profile_key = (original_profile_name, profile_return_code)
            if new_profile_key not in failed_profile_map:
                if original_profile_name not in profiles:
                    print(f"Error: Profile '{original_profile_name}' not found in workload's 'profiles' section. Cannot create failing variant for job {job.get('id', i)}.")
                    continue # Skip this job if its profile is missing

                original_profile_data = profiles[original_profile_name]
                new_profile_name = f"{original_profile_name}_failed_{profile_return_code}_{len(failed_profile_map)}"
                
                # Deep copy the original profile to avoid modifying it directly
                new_profile_data = json.loads(json.dumps(original_profile_data)) 
                
                # Set the 'ret' field in the new profile
                new_profile_data['ret'] = profile_return_code
                
                profiles[new_profile_name] = new_profile_data
                failed_profile_map[new_profile_key] = new_profile_name
            
            # Update the job's profile to point to the new failing profile
            job['profile'] = failed_profile_map[new_profile_key]
            
            # The 'return_code' field in the job object itself is not directly used by Batsim
            # for simulation outcome, but is useful for the scheduler to quickly identify
            # the intended outcome and any associated metadata. We'll keep it for clarity.
            job['return_code'] = profile_return_code 
        else:
            # Ensure successful jobs explicitly have a return_code of 0 in the job object
            # (though Batsim's profile 'ret' is what truly determines success)
            job['return_code'] = 0


    print(f"--- Simulation Summary ---")
    print(f"Total jobs in workload: {num_jobs}")
    print(f"Target general job failure rate range: {job_failure_rate_range[0]:.2f}% - {job_failure_rate_range[1]:.2f}%")
    print(f"Actual general job failure rate applied: {(num_general_failures + num_critical_failures) / num_jobs * 100:.2f}%")
    print(f"Number of jobs marked for general failure: {num_general_failures + num_critical_failures}")
    print(f"Target critical failure rate (of failed jobs) range: {critical_failure_rate_range[0]:.2f}% - {critical_failure_rate_range[1]:.2f}%")
    if (num_general_failures + num_critical_failures) > 0:
        actual_critical_rate_of_failed = (num_critical_failures / (num_general_failures + num_critical_failures)) * 100
        print(f"Actual critical failure rate (of all failed jobs) applied: {actual_critical_rate_of_failed:.2f}%")
    else:
        print("No general job failures, so no critical failures could be applied.")
    print(f"Number of jobs marked as critical/node-induced failures: {num_critical_failures}")
    print(f"Number of new profiles created for failures: {len(failed_profile_map)}")
    print(f"--------------------------")

    # Update the workload object with the modified jobs list and new profiles
    workload['jobs'] = jobs
    workload['profiles'] = profiles

    try:
        with open(output_workload_path, 'w') as f:
            json.dump(workload, f, indent=2)
        print(f"Modified workload successfully saved to: {output_workload_path}")
    except IOError as e:
        print(f"Error: Could not write to output file '{output_workload_path}'. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing the output file: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Simulate random job and 'critical' (node-induced) failures in a Batsim workload JSON file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "input_workload",
        help="Path to the input Batsim workload JSON file (e.g., workloads/test_workload_profile.json)."
    )
    parser.add_argument(
        "output_workload",
        help="Path to save the modified Batsim workload JSON file (e.g., modified_workload.json)."
    )
    parser.add_argument(
        "--job-failure-min",
        type=float,
        default=3.0,
        help="Minimum percentage (0-100) of all jobs to mark as generally failed.\n"
            "Default: 3.0"
    )
    parser.add_argument(
        "--job-failure-max",
        type=float,
        default=15.0,
        help="Maximum percentage (0-100) of all jobs to mark as generally failed.\n"
            "Default: 15.0"
    )
    parser.add_argument(
        "--critical-failure-min",
        type=float,
        default=10.0,
        help="Minimum percentage (0-100) of *already failed jobs* to mark as critical (node-induced).\n"
            "These jobs will have return_code=99 and 'failure_type: node_induced' metadata.\n"
            "Default: 10.0"
    )
    parser.add_argument(
        "--critical-failure-max",
        type=float,
        default=30.0,
        help="Maximum percentage (0-100) of *already failed jobs* to mark as critical (node-induced).\n"
            "Default: 30.0"
    )

    args = parser.parse_args()

    simulate_failures(
        args.input_workload,
        args.output_workload,
        (args.job_failure_min, args.job_failure_max),
        (args.critical_failure_min, args.critical_failure_max)
    )
