import subprocess
import time
from flask import Flask, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from celery import Celery

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
    job = db_session.query(Job).filter(Job.id == job_id).one()
    job.status = "running"
    job.start_time = int(time.time())
    db_session.commit()

    try:
        process = subprocess.Popen(script, shell=True)
        process.wait()
        job.status = "completed"
    except subprocess.CalledProcessError:
        job.status = "failed"

    job.end_time = int(time.time())
    db_session.commit()
    db_session.close()


class JobResource(Resource):
    def post(self):
        script = request.form['script']
        job = Job(script=script, status="queued")
        db_session.add(job)
        db_session.commit()
        execute_job.delay(job.id, script)
        return {"job_id": job.id}

    def get(self, job_id):
        job = db_session.query(Job).filter(Job.id == job_id).one()
        return {"job_id": job.id,
                "status": job.status,
                "start_time": job.start_time,
                "end_time": job.end_time}

    def delete(self, job_id):
        job = db_session.query(Job).filter(Job.id == job_id).one()
        if job.status == "running":
            execute_job.AsyncResult(job_id).revoke(terminate=True)
            job.status = "failed"
            db_session.commit()
        return {"result": "Job terminated"}

api.add_resource(JobResource, '/job', '/job/<int:job_id>')

if __name__ == '__main__':
    app.run(debug=True)
