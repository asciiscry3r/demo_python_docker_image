FROM python:3

WORKDIR /usr/src/app

RUN pip3 install --upgrade pip --root-user-action ignore && pip3 install redis --root-user-action ignore

COPY . .

EXPOSE 8080
