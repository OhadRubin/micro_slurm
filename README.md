To test if everything is working correctly, you can submit a job, monitor its status, and interrupt a running job using HTTP requests. You can use curl to send requests from the command line or use an API testing tool like Postman.

Here are examples using curl to test the different functionalities:

Submit a job: Send a POST request to the /job endpoint with the job script as form data. Replace <job_script> with your desired script or command.

sh
Copy code
curl -X POST -F "script=<job_script>" <http://localhost:5000/job>
You should receive a response containing the job_id. Take note of the job_id for the next steps.

Monitor job status: Send a GET request to the /job/<job_id> endpoint, replacing <job_id> with the ID from the previous step.

sh
Copy code
curl -X GET <http://localhost:5000/job/<job_id>>
You should receive a response with the job status and timestamps. Check the status to see if the job is queued, running, completed, or failed.

Interrupt a running job: To test job interruption, submit a long-running job using the first step. While the job is running, send a DELETE request to the /job/<job_id> endpoint, replacing <job_id> with the ID of the running job.

sh
Copy code
curl -X DELETE <http://localhost:5000/job/<job_id>>
You should receive a response indicating that the job has been terminated. Check the job status again using the second step to confirm that the status has been updated to "failed".

By submitting a job, monitoring its status, and interrupting a running job, you can verify that the MicroSlurm 1.0 MVP is working as expected.
