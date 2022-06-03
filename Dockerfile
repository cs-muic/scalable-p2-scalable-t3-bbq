# start from base
FROM python:3.9

# copy our application code
COPY ./vid2gif.py /togif/vid2gif.py
COPY ./requirements.txt /togif/requirements.txt
WORKDIR /togif

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Install dependencies
RUN pip install -r requirements.txt

# Assign execution permissions
RUN chmod +x vid2gif.py

RUN mkdir "/images"
