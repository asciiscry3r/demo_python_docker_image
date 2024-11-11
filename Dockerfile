FROM python:3

WORKDIR /usr/src/app

RUN pip install redis

COPY . .

CMD [ "python", "server.py", "-l 127.0.0.1", "-p 8080" ]