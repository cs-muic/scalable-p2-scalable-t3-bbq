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

# generate bucket of videos
found = MINIO_CLIENT.bucket_exists("videos")
if not found:
    MINIO_CLIENT.make_bucket("videos")


def get_frames(fp_in):

    # generate bucket of frames extracted
    s = 10  # number of characters in the string.
    randstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=s))
    found = MINIO_CLIENT.bucket_exists(randstr)
    if not found:
        MINIO_CLIENT.make_bucket(randstr)
    else:
        print("Bucket already exists")

    MINIO_CLIENT.fput_object("videos", object_name=os.path.basename(fp_in), file_path=fp_in)
    vidcap = cv2.VideoCapture(fp_in)
    # fps = vidcap.get(cv2.CAP_PROP_FPS)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    success, image = vidcap.read()
    count = 0
    while success:
        if 1 / 3 * length < count < 1 / 3 * length + 15 * 15:
            frame = imutils.resize(image, width=480)
            cv2.imwrite("../images/frame%d.png" % count, frame)
            MINIO_CLIENT.fput_object(randstr, object_name="frame%d.png" % count,
                                     file_path="../images/frame%d.png" % count)
            try:
                os.remove("../images/frame%d.png" % count)
            except:
                pass
        success, image = vidcap.read()
        count += 1

    return print("Successfully uploaded all frames to bucket")


if __name__ == '__main__':
    fp_in = sys.argv[1]
    get_frames(fp_in)
