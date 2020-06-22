FROM python:3.8

RUN pip install python-telegram-bot==12.7

ADD src /src/
CMD [ "python", "./src/main.py" ]
