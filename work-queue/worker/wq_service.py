import os
import time

from celery import Celery
from celery.result import AsyncResult
from dotenv import load_dotenv
from minio import Minio

import compose
import extract

BROKER_URL = os.environ.get("CELERY_BROKER_URL",
                            "redis://localhost:6378/0"),
RES_BACKEND = os.environ.get("CELERY_RESULT_BACKEND",
                             "db+postgresql://dbc:dbc@localhost:5434/celery")

celery_app = Celery('wq-service', broker=BROKER_URL,
                    backend=RES_BACKEND)

load_dotenv()

LOCAL_FILE_PATH = os.environ.get('LOCAL_FILE_PATH')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

MINIO_API_HOST = "http://localhost:9000"
MINIO_URL = os.environ.get("MINIO_URL")

MINIO_CLIENT = Minio(MINIO_URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)


def issue_tasks(worker, param):
    global extract_q, compose_q
    if worker == 'extract':
        task = extract.celery_app.send_task('extract.get_frames', queue='q01', kwargs={'fp_in': param})
        extract_q.append(task.task_id)
        return task.task_id
    elif worker == 'compose':
        task = compose.celery_app.send_task('compose.to_gif', queue='q02', kwargs={'bucket_name': param})
        compose_q.append(task.task_id)
        return task.task_id


def add_to_eq(video):
    issue_tasks('extract', video)


def convert_bucket(bucket_name):
    videos = MINIO_CLIENT.list_objects(bucket_name=bucket_name)
    for vid in videos:
        add_to_eq(vid)


def list_gif():
    return MINIO_CLIENT.list_objects(bucket_name='gif')


def get_progress(tid):
    return get_results(tid)


def get_results(task_id):
    task_result = AsyncResult(task_id)
    result = {
        'task_id': task_id,
        'task_status': task_result.status,
        'task_result': task_result.result,
    }
    return result


if __name__ == "__main__":

    extract_q = []
    compose_q = []
    buckets = []

    add_to_eq("./test3.mp4")

    while 1:
        done = True
        for tid in extract_q:
            res = get_results(tid)
            if res['task_status'] == 'SUCCESS':
                buckets.append(res["task_result"])
                extract_q.remove(tid)
                compose_q.append(issue_tasks('compose', res["task_result"]))
                print(f'queue: q01, task: {tid}, result: {res["task_result"]}')
            elif res['task_status'] == 'FAILURE':
                print(f'queue: q01, task: {tid}, result: {res["task_result"]}')
            else:
                done = False
                print(f'queue: q01, task: {tid}, status: {res["task_status"]}')
                time.sleep(5)

        for tid in compose_q:
            res = get_results(tid)
            if res['task_status'] == 'SUCCESS' or \
                    res['task_status'] == 'FAILURE':
                compose_q.remove(tid)
                print(f'queue: q02, task: {tid}, result: {res["task_result"]}')
            else:
                done = False
                print(f'queue: q02, task: {tid}, status: {res["task_status"]}')
                time.sleep(5)
