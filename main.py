import time
from collections import deque
from uuid import uuid4

class Job:
    def __init__(self, resources, runtime, dependencies=None):
        self.id = str(uuid4())
        self.resources = resources
        self.runtime = runtime
        self.dependencies = dependencies if dependencies else []
        self.status = "queued"
        self.start_time = None
        self.end_time = None
        self.resource_usage = None

class JobQueue:
    def __init__(self):
        self.jobs = {}

    def add_job(self, job):
        self.jobs[job.id] = job

    def remove_job(self, job_id):
        del self.jobs[job_id]

    def update_job_status(self, job_id, status):
        self.jobs[job_id].status = status

    def get_job(self, job_id):
        return self.jobs.get(job_id)

    def get_all_jobs(self):
        return self.jobs.values()

    def get_dependent_jobs(self, job_id):
        return [job for job in self.jobs.values() if job_id in job.dependencies]

class ResourceManager:
    def __init__(self, total_resources):
        self.total_resources = total_resources
        self.used_resources = 0

    def allocate_resources(self, resources):
        self.used_resources += resources

    def release_resources(self, resources):
        self.used_resources -= resources

    def available_resources(self):
        return self.total_resources - self.used_resources

class Scheduler:
    def __init__(self, job_queue, resource_manager):
        self.job_queue = job_queue
        self.resource_manager = resource_manager

    def process_jobs(self):
        while self.job_queue.jobs:
            for job in self.job_queue.get_all_jobs():
                if job.status == "queued" and self.all_dependencies_completed(job) and self.resource_manager.available_resources() >= job.resources:
                    self.resource_manager.allocate_resources(job.resources)
                    self.job_queue.update_job_status(job.id, "running")
                    job.start_time = time.time()

                    # Simulate job execution
                    time.sleep(job.runtime)

                    job.end_time = time.time()
                    job.resource_usage = job.resources
                    self.resource_manager.release_resources(job.resources)
                    self.job_queue.update_job_status(job.id, "completed")

            # Remove completed jobs from the queue
            completed_jobs = [job.id for job in self.job_queue.get_all_jobs() if job.status == "completed"]
            for job_id in completed_jobs:
                self.job_queue.remove_job(job_id)

    def all_dependencies_completed(self, job):
        return all(self.job_queue.get_job(dep_id).status == "completed" for dep_id in job.dependencies)

# Example usage
resources = 10
total_runtime = 2
job_queue = JobQueue()
resource_manager = ResourceManager(resources)
scheduler = Scheduler(job_queue, resource_manager)

# Submitting jobs
job1 = Job(resources=4, runtime=2)
job2 = Job(resources=4, runtime=2, dependencies=[job1.id])

job_queue.add_job(job1)
job_queue.add_job(job2)

# Running the scheduler
scheduler.process_jobs()

# Querying job status
for job in job_queue.get_all_jobs():
    print(f"Job ID: {job.id}, Status: {job.status}")

