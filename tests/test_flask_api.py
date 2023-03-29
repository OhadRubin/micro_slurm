# tests/test_flask_api.py

import json
import pytest
from microslurm import Job, db_session


def test_post_job(client):
    response = client.post('/job', data={"script": "echo 'Hello, World!'"})
    assert response.status_code == 200

    response_data = json.loads(response.data)
    job_id = response_data["job_id"]
    job = db_session.query(Job).filter(Job.id == job_id).one()
    assert job.script == "echo 'Hello, World!'"
    assert job.status == "queued"


def test_get_job(client):
    script = "echo 'Hello, World!'"
    job = Job(script=script, status="queued")
    db_session.add(job)
    db_session.commit()

    response = client.get(f'/job/{job.id}')
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data["job_id"] == job.id
    assert response_data["status"] == "queued"


def test_delete_job(client):
    script = "echo 'Hello, World!'"
    job = Job(script=script, status="queued")
    db_session.add(job)
    db_session.commit()

    response = client.delete(f'/job/{job.id}')
    assert response.status_code ==200
    response_data = json.loads(response.data)
    assert response_data["result"] == "Job terminated"

    deleted_job = db_session.query(Job).filter(Job.id == job.id).one()
    assert deleted_job.status == "failed"
