To complete MicroSlurm 1.0, we will follow the detailed pseudocode plan:

Import required libraries (SQLAlchemy, Flask-RESTful, Celery, argparse)
Define the database schema for Job and JobDependency using SQLAlchemy
Initialize the SQLite database with the defined schema
Create a Celery instance for job execution and management
Define a function to execute a job using Celery
a. Accept the job script
b. Execute the job
c. Return the result and resource usage
Define a function to submit a job
a. Accept job details, such as the job script, resources, and any dependencies
b. Create a new Job entry in the database
c. If there are job dependencies, create JobDependency entries in the database
d. If there are no dependencies or all dependencies have been completed, schedule the job for execution using Celery
Define a function to monitor job status
a. Query the database for the job status
b. Return the status (queued, running, completed, failed)
Define a function to interrupt a job
a. Accept the job ID
b. Use Celery to terminate the job
c. Update the job status in the database to "failed"
Define a function for logging and reporting
a. Log the job execution details, such as start time, end time, and resource usage, in the database
Create a REST API using Flask-RESTful
a. Define API endpoints for job submission, job monitoring, job interruption, and logging
b. Implement the API endpoints using the previously defined functions
Implement a command-line interface using argparse
a. Define command-line options for job submission, job monitoring, job interruption, and logging
b. Call the corresponding API endpoints based on the user's command-line input
Define a function to handle job dependencies
a. Check the status of dependent jobs
b. If all dependent jobs are completed, schedule the job for execution using Celery
Set up periodic task in Celery to check and handle job dependencies
Add exception handling and error messages for different scenarios, such as invalid input or job script errors
With this detailed plan, you can extend the basic implementation provided earlier to complete the full functionality of MicroSlurm 1.0 library.