FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

COPY . /app/