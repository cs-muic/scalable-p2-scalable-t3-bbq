FROM python:3.9-slim

WORKDIR /usr/src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./requirements.txt .
COPY ./test3.mp4 .
COPY ./wq_service.py .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt


