FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y build-essential libpq-dev postgresql-client
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY .env.docker.example /code/.env
