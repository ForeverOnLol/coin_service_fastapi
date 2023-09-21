FROM python:3.9

# set work directory
WORKDIR /fast_api

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN apt-get update
RUN pip install -r requirements.txt