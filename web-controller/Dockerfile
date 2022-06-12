FROM python:3.9-slim

WORKDIR /usr/src/


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

ADD ../ .

RUN pip install --upgrade pip
COPY requirements.txt .
COPY ./backend.py .

RUN pip install -r requirements.txt

#CMD python /usr/src/web-controller/backend.py
