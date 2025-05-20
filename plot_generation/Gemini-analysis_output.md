# Analysis
Okay, let's analyze these two charts as a data scientist.

**Chart 1: Jobs Submitted per User**

**Description:** This is a stacked bar chart showing the number of jobs submitted by each user, broken down by the final state of the job (FAILED, COMPLETED, CANCELLED, NODE_FAIL, TIMEOUT).  The x-axis represents the User ID, and the y-axis represents the number of jobs submitted.

**Key Observations and Quantitative Analysis:**

*   **User 58707 is the High-Volume Submitter:**  This user clearly submitted the most jobs, significantly more than any other user. Approximately 102 jobs in total.

*   **User 58707 has high rates of failure:** The biggest part of user 58707's submissions were completed(approx 56), but also had significant rates of cancellation and node failure, making it a very large amount of submissions for this user.

*   **Completion rates vary across users:**  For example, User 58584 has a substantial number of completed jobs (around 23), but also a significant number of failed jobs.  Other users, like 14972, have very few jobs submitted overall.

*   **User 58467 has high rates of failure:** Similar to user 58707, this user has a large amount of failures, at around 15 failures.

*   **Overall Distribution:** Most users submit a relatively small number of jobs, but a few users contribute a large proportion of the overall job submissions. This distribution is likely skewed right.

*   **Calculating Total Jobs and Percentages:**

    *   We can approximate the total number of jobs submitted across all users by summing the heights of each bar. Summing the heights of each bar gives a grand total of roughly 200 jobs
    *   We can approximate the percentage of total jobs that failed, completed, cancelled, node fail and timed out.
        *   Failed: 15%
        *   Completed: 50%
        *   Cancelled: 5%
        *   Node Fail: 25%
        *   Timeout: 5%

**Chart 2: Wait Time vs. JobID**

**Description:** This chart is a scatter plot depicting the wait time (in seconds) for each job, plotted against the JobID. Different job states are represented by different colors. It shows each job's ID and what state it transitioned to from wait time.

**Key Observations and Quantitative Analysis:**

*   **Failed Jobs have much higher wait times:** The Failed jobs show to have a much higher wait time when compared to other states, with a high of nearly 55 seconds of wait time.

*   **Most Jobs have very low wait times:** Many of the data points cluster near the bottom of the graph, indicating that most jobs have a wait time close to zero seconds.

*   **Outlier:** There is a completed job from around jobID 3140 to have a very high wait time of nearly 35 seconds.

**Relationships and Combined Analysis:**

Combining the insights from both charts, we can start to formulate some hypotheses:

*   **User 58707's High Job Submission Volume:** This user is generating many failed, cancelled, and node fail jobs. Analyzing the code/scripts used by this user might reveal why these jobs are failing or being cancelled.

*   **Correlation between User, Job State, and Wait Time:** Explore the correlation between UserID, JobState, and WaitTime. You could compute correlation coefficients or use ANOVA if JobState is considered a categorical variable.

*   **Why are the Failed Jobs of User 58707 having such a high wait time?:** Is it the same code that causes them to fail or is there some other reason they take longer to execute.

**Next Steps and Recommendations:**

*   **Investigate User 58707:**  Examine the code and scripts submitted by User 58707. Look for patterns in the failed jobs. Are there specific types of calculations or data sources that are causing failures?
*   **Look at the correlation between user ID, job states and wait time:** See what the correlation is and if the job states have an affect on wait time.
*   **Further data:** More details about the jobs themselves like the user, time submitted and resources used would be helpful for deeper analysis.
*   **Time series Analysis:** If the data includes timestamps, you could perform time series analysis to identify patterns and trends in job submissions, failure rates, and wait times over time.
*   **Resource Utilization:** Consider adding resource usage metrics (CPU, memory, disk I/O) to the data to identify potential bottlenecks and optimize resource allocation.

By combining these statistical observations with deeper domain knowledge and further data, we can develop actionable strategies to optimize job execution, improve resource utilization, and reduce failure rates.
