# tests/test_celery_task.py

import pytest
from microslurm import execute_job, Job, db_session


def test_execute_job():
    script = "echo 'Hello, World!'"
    job = Job(script=script, status="queued")
    db_session.add(job)
    db_session.commit()

    execute_job(job.id, script)

    completed_job = db_session.query(Job).filter(Job.id == job.id).one()
    assert completed_job.status == "completed"
