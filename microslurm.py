import os
import subprocess
import time
from flask import Flask, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from celery import Celery
from celery.result import AsyncResult
from sqlalchemy.orm.exc import NoResultFound


# Database setup
engine = create_engine('postgresql://microslurm:microslurm@postgres/microslurm_db')

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

app = Flask(__name__)
api = Api(app)

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    script = Column(String)
    status = Column(String)
    start_time = Column(Integer)
    end_time = Column(Integer)

Base.metadata.create_all(engine)

celery_app = Celery('microslurm', broker='pyamqp://guest@rabbitmq//')

@celery_app.task
def execute_job(job_id, script):
    worker_session = sessionmaker(bind=engine)()

    job = worker_session.query(Job).filter(Job.id == job_id).one()
    job.status = "running"
    job.start_time = int(time.time())
    worker_session.commit()

    try:
        process = subprocess.Popen(script, shell=True)
        return_code = process.wait()
        if return_code == 0:
            job.status = "completed"
        else:
            job.status = "failed"
    except subprocess.CalledProcessError:
        job.status = "failed"
        worker_session.rollback()
    except Exception as e:
        job.status = "failed"
        print(f"Unexpected error occurred: {e}")
        worker_session.rollback()


    job.end_time = int(time.time())
    worker_session.commit()
    worker_session.close()


class JobResource(Resource):
    def post(self):
        script = request.form['script']
        job = Job(script=script, status="queued")
        db_session.add(job)
        db_session.commit()
        execute_job.delay(job.id, script)
        return {"job_id": job.id}

    def get(self, job_id):
        try:
            job = db_session.query(Job).filter(Job.id == job_id).one()
        except NoResultFound:
            return {"error": "Job not found"}, 404
        return {"job_id": job.id,
                "status": job.status,
                "start_time": job.start_time,
                "end_time": job.end_time}

    def delete(self, job_id):
        try:
            job = db_session.query(Job).filter(Job.id == job_id).one()
        except NoResultFound:
            return {"error": "Job not found"}, 404
        if job.status == "running":
            result = AsyncResult(job_id, app=celery_app)
            result.revoke(terminate=True)
            job.status = "failed"
            db_session.commit()
        return {"result": "Job terminated"}

api.add_resource(JobResource, '/job', '/job/<int:job_id>')

if __name__ == '__main__':
    app.run(debug=os.environ.get("FLASK_DEBUG", False))

