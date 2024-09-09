FROM python:3.10-slim-buster

WORKDIR /ATLAS CBT APP

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /ATLAS CBT APP/APP
