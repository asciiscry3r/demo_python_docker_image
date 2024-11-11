FROM python:3

WORKDIR /usr/src/app

RUN pip install redis

COPY . .

EXPOSE 8080

CMD [ "/usr/bin/python", "/usr/src/app/server.py", "-l 127.0.0.1", "-p 8080" ]