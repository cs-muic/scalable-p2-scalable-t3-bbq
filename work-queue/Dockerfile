FROM python:3.9-slim

WORKDIR /usr/src/


RUN apt-get update

RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY backend.py .
RUN pip install -r requirements.txt

RUN mkdir -p /usr/src/worker
COPY ./worker /usr/src/worker

CMD python ./backend.py