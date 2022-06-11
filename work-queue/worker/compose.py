import glob
from PIL import Image
import sys
from minio import Minio
from dotenv import load_dotenv
import os
from celery import Celery
import shutil

BROKER_URL = 'redis://localhost:6379'

celery_app = Celery('Extract', broker=BROKER_URL)

load_dotenv()

LOCAL_FILE_PATH = os.environ.get('LOCAL_FILE_PATH')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

MINIO_API_HOST = "http://localhost:9000"

MINIO_CLIENT = Minio("localhost:9000", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

# generate bucket of GIF
found = MINIO_CLIENT.bucket_exists("gif")
if not found:
    MINIO_CLIENT.make_bucket("gif")


@celery_app.task
def to_gif(fp_out):

    bucket_name = "039p2zot4j"

    frames = MINIO_CLIENT.list_objects(bucket_name=bucket_name, prefix="frame")

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif

    os.mkdir(bucket_name)
    for obj in frames:
        fp = bucket_name + "/" + obj.object_name
        MINIO_CLIENT.fget_object(bucket_name=bucket_name, object_name=obj.object_name, file_path=fp)

    frames = bucket_name + "/frame*.png"

    imgs = (Image.open(f) for f in sorted(glob.glob(frames)))
    img = next(imgs)  # extract first image from iterator

    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=1 / 15, loop=0)

    MINIO_CLIENT.fput_object("gif", object_name=fp_out, file_path=fp_out, content_type="image/gif")

    os.remove(fp_out)
    shutil.rmtree(bucket_name)


if __name__ == '__main__':
    fp_out = sys.argv[1]
    # fp_in = sys.argv[2]
    to_gif(fp_out)