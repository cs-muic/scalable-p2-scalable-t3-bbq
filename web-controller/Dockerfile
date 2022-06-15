FROM python:3.9-slim

WORKDIR /usr/src

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

#ADD ../ .

RUN pip install --upgrade pip
COPY ./web-controller/requirements.txt .
COPY ./web-controller/backend.py .
COPY ./work_queue/worker/extract_w/extract.py ./work_queue/worker/extract_w

RUN pip install -r requirements.txt

#CMD python /usr/src/web-controller/backend.py
