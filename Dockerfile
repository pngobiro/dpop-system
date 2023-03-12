FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /code


# install  apt-utils ,  FFmpeg for audio and video processing
RUN apt-get update && apt-get install -y apt-utils ffmpeg


# copy requirements.txt to workdir and install dependencies
COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# copy project to workdir

COPY . /code/




# run docker bash



