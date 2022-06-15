FROM python:3.9-slim

WORKDIR /usr/src/work_queue/worker

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY ./work_queue/worker/ .

RUN pip install -r requirements.txt
