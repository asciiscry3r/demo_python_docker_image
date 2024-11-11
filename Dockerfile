FROM python:3

WORKDIR /usr/src/app

RUN pip3 install --upgrade pip --root-user-action ignore && pip3 install redis --root-user-action ignore

COPY . .

EXPOSE 8080

CMD [ "python3", "server.py", "-l 127.0.0.1", "-p 8080" ]