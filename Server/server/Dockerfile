FROM python:3.10-slim-buster
WORKDIR /app


RUN apt-get  -y update &&  \
    apt-get install -y curl &&  \
    apt-get install -y less && \
    apt-get install -y iputils-ping

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

RUN mkdir -p /opt/app/data && \
    mkdir -p /opt/app/logs

VOLUME ["/opt/app/data"]
VOLUME ["/opt/app/logs"]


CMD [ "python3", "main.py"]
