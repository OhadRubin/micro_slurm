# tests/test_database.py

import pytest
from microslurm import Job, db_session


def test_create_job():
    script = "echo 'Hello, World!'"
    job = Job(script=script, status="queued")
    db_session.add(job)
    db_session.commit()

    saved_job = db_session.query(Job).filter(Job.id == job.id).one()
    assert saved_job.script == script
    assert saved_job.status == "queued"


def test_update_job_status():
    script = "echo 'Hello, World!'"
    job = Job(script=script, status="queued")
    db_session.add(job)
    db_session.commit()

    job.status = "running"
    db_session.commit()

    updated_job = db_session.query(Job).filter(Job.id == job.id).one()
    assert updated_job.status == "running"
