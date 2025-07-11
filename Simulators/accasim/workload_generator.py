from accasim.experimentation.workload_generator import workload_generator
import accasim.experimentation.workload_generator

'''

SWF file format specification (18 fields):
; 1. Job ID: a counter field, starting from 1.
; 2. Submit Time: in seconds. The earliest time the log refers to is zero.
; 3. Wait Time: in seconds. The difference between the job's submit time and its actual start time.
; 4. Run Time: in seconds. The wall clock time the job was running (end time minus start time).
; 5. Number of Allocated Processors: an integer. In most cases, this is also the number of processors the job uses.
; 6. Average CPU Time Used: both user and system, in seconds. Average over all processors.
; 7. Used Memory: in kilobytes. Average per processor.
; 8. Requested Number of Processors.
; 9. Requested Time: This can be either runtime (wallclock seconds) or average CPU time per processor.
; 10. Requested Memory: in kilobytes per processor.
; 11. Status: 1 if the job was completed, 0 if it failed, 5 if cancelled.
; 12. User ID: a natural number.
; 13. Group ID: a natural number.
; 14. Executable (Application) Number: a natural number.
; 15. Queue Number: a natural number.
; 16. Partition Number: a natural number.
; 17. Preceding Job Number: ID of a previous job this job depends on (-1 if no dependency).
; 18. Think Time from Preceding Job: time in seconds after preceding job finishes until this one is submitted.

'''
    
if __name__ == '__main__':
    #===========================================================================
    # Workload filepath
    #===========================================================================
    workload = 'workload.swf'
    
    #==========================================================================
    # System config filepath
    #==========================================================================
    sys_config = '/home/er3/ORNL-Work/Simulators/accasim/config/HPC2N.config'
    
    #===========================================================================
    # Performance of the computing units
    #===========================================================================
    performance = { 'core': 3.334 / 2 }
    
    #===========================================================================
    # Request limits for each resource type
    #===========================================================================
    request_limits = {'min':{'core': 1, 'mem': 1000000 // 4}, 'max': {'core': 4, 'mem': 1000000}}
    
    #===========================================================================
    # Create the workload generator instance with the basic inputs
    #===========================================================================
    generator = workload_generator(workload, sys_config, performance, request_limits)
    #===========================================================================
    # Generate n jobs and save them to the nw filepath
    #===========================================================================
    n = 100
    nw_filepath = './new_workload.swf'
    jobs = generator.generate_jobs(n, nw_filepath)
    