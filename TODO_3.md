Given the requirements, I will create a detailed pseudocode plan for the MicroSlurm 1.0 library, which will be a lightweight job management and scheduling library in Python. We will use existing libraries such as SQLAlchemy, Flask-RESTful, and Celery.

Pseudocode:

Import required libraries (SQLAlchemy, Flask-RESTful, Celery)
Define the database schema for Job and JobDependency using SQLAlchemy
Initialize the SQLite database with the defined schema
Create a Celery instance for job execution and management
Define a function to submit a job
a. Accept job details, such as the job script, resources, and any dependencies
b. Create a new Job entry in the database
c. If there are job dependencies, create JobDependency entries in the database
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
Implement a command-line interface
a. Define command-line options for job submission, job monitoring, job interruption, and logging
b. Call the corresponding API endpoints based on the user's command-line input
