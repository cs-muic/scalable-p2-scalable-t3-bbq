import json

from flask import jsonify, request, Flask
from celery import Celery
from celery.result import AsyncResult
from minio import Minio
import os

from work_queue.worker.extract_w import extract
from work_queue.worker.compose_w import compose

ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')

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
def convert():
    global eq
    video = request.json["video"]
    task = extract.celery_app.send_task('extract.get_frames', queue='q01', kwargs={'fp_in': video})
    eq.append(task.task_id)
    return "Converting"


@app.route('/convert-bucket', methods=['POST'])
def convert_all():
    global eq
    bucket_name = request.json["bucket_name"]
    all_vid = MINIO_CLIENT.list_objects(bucket_name=bucket_name)
    for vid in all_vid:
        MINIO_CLIENT.fget_object(bucket_name=bucket_name, object_name=vid.object_name, file_path=vid.object_name)
        task = extract.celery_app.send_task('extract.get_frames', queue='q01', kwargs={'fp_in': vid.object_name})
        eq.append(task.task_id)
    return "Converting all videos inside the bucket"


@app.route('/list-gif')
def list_gif():
    for obj in MINIO_CLIENT.list_objects(bucket_name='gif'):
        MINIO_CLIENT.fget_object(bucket_name='gif', object_name=obj.object_name, file_path=obj.object_name)
    return 'f'


@app.route('/track', methods=['POST'])
def track():
    global eq, cq

    for task in eq:
        res = AsyncResult(task)
        if (res.state == "SUCCESS") and (res.result not in cq):
            cq.append(res.result)
    obj = json.dumps({"extract_q": eq, "compose_q": cq})

    try:
        tid = request.json["tid"]
    except:
        return obj

    if tid not in eq:
        return obj
    else:
        task_result = AsyncResult(tid)
        return task_result.state


if __name__ == "__main__":
    eq = []
    cq = []
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
