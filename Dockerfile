FROM python:3.10

RUN apt update -y && apt upgrade -y

COPY . /telebot_1.py
COPY . /requirements.txt

WORKDIR /telebot_1.py

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD python3 telebot_1.py
