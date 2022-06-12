FROM python:3.9-slim

WORKDIR /usr/src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
#COPY ./worker/compose-w/compose.py .
RUN pip install -r requirements.txt

COPY ./worker/wq_service.py .