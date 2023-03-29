import os
import subprocess
import time
from flask import Flask, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from celery import Celery

# Database setup
Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    script = Column(String)
    status = Column(String)
    start_time = Column(Integer)
    end_time = Column(Integer)

engine = create_engine('sqlite:///microslurm.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Celery setup
celery_app = Celery('microslurm', broker='pyamqp://guest@rabbitmq//')


@celery_app.task
def execute_job(job_id, script):
    session = Session()
    job = session.query(Job).filter(Job.id == job_id).one()
    job.status = "running"
    job.start_time = int(time.time())
    session.commit()

    try:
        # subprocess.check_call(script, shell=True)
        process = subprocess.Popen(script, shell=True)
        process.wait()
        job.status = "completed"
    except subprocess.CalledProcessError:
        job.status = "failed"

    job.end_time = int(time.time())
    session.commit()
    session.close()

# REST API setup
app = Flask(__name__)
api = Api(app)

class JobResource(Resource):
    def post(self):
        script = request.form['script']
        job = Job(script=script, status="queued")
        session = Session()
        session.add(job)
        session.commit()
        execute_job.delay(job.id, script)
        return {"job_id": job.id}

    def get(self, job_id):
        session = Session()
        job = session.query(Job).filter(Job.id == job_id).one()
        return {"job_id": job.id, "status": job.status, "start_time": job.start_time, "end_time": job.end_time}

    def delete(self, job_id):
        session = Session()
        job = session.query(Job).filter(Job.id == job_id).one()
        if job.status == "running":
            execute_job.AsyncResult(job_id).revoke(terminate=True)
            job.status = "failed"
            session.commit()
        return {"result": "Job terminated"}

api.add_resource(JobResource, '/job', '/job/<int:job_id>')

if __name__ == '__main__':
    app.run(debug=True)
