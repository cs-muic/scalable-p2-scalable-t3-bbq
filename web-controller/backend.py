from flask import Flask
from celery import Celery
from celery.result import AsyncResult
from dotenv import load_dotenv
from minio import Minio
import os

from work_queue.worker.extract_w import extract
from work_queue.worker.compose_w import compose

load_dotenv()

LOCAL_FILE_PATH = os.environ.get('LOCAL_FILE_PATH')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

MINIO_API_HOST = "http://localhost:9000"
MINIO_URL = os.environ.get("MINIO_URL")

# CHANGE to MINIOURL
MINIO_CLIENT = Minio(MINIO_URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)


app = Flask(__name__)


@app.route('/')
def index():
    # return "Hello Video Thumbnailer!!"
    return 'f'


# submit jobs to the queue
@app.route('/convert', methods=['POST'])
def convert(video):
    extract.celery_app.send_task('extract.get_frames', queue='q01', kwargs={'fp_in': video})
    return 'wtf'


@app.route('/convert-bucket', methods=['GET'])
def convert_all():
    return "Converting all videos inside the bucket"


@app.route('/list-gif')
def list_gif():
    return MINIO_CLIENT.list_objects(bucket_name='gif')


@app.route('/track')
def track(tid):
    task_result = AsyncResult(tid)
    return task_result.result


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
