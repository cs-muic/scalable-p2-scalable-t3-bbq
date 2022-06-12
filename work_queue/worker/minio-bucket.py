import cv2
import imutils
import sys
import string
import random
import os
from minio import Minio
from dotenv import load_dotenv

load_dotenv()

LOCAL_FILE_PATH = os.environ.get('LOCAL_FILE_PATH')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

MINIO_API_HOST = "http://localhost:9000"

MINIO_CLIENT = Minio("localhost:9000", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

bucket = "6zp4jc2dih"

for f in MINIO_CLIENT.list_objects(bucket):
    MINIO_CLIENT.remove_object(bucket, f.object_name)

MINIO_CLIENT.remove_bucket(bucket)
