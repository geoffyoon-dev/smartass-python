FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt upgrade -y &&\
    apt install sudo -y &&\
    apt install software-properties-common -y &&\
    apt install vim -y &&\
    add-apt-repository ppa:deadsnakes/ppa &&\
    apt update && apt install python3.12 -y &&\
    apt install python3-pip -y &&\
    apt install python3-dev -y &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

WORKDIR /home/ubuntu/app
RUN chmod -R 777 /home/ubuntu/app

RUN echo "ubuntu:ubuntu" | chpasswd && usermod -aG sudo ubuntu
USER ubuntu
WORKDIR /home/ubuntu

RUN python -m pip config set global.break-system-packages true

COPY requirements.txt /home/ubuntu/app/requirements.txt
WORKDIR /home/ubuntu/app
RUN pip install -r requirements.txt

COPY setup.py /home/ubuntu/app/setup.py

COPY smartass /home/ubuntu/app/smartass