FROM python:3.9-slim

WORKDIR /usr/src/


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY backend.py .
#COPY ./worker/wq_service.py .
#COPY ./worker/test3.mp4 .
COPY ./worker ./worker
RUN pip install -r requirements.txt

RUN mkdir -p /usr/src/worker
COPY ./worker /usr/src/worker

CMD python backend.py &
CMD python ./worker/wq_service.py