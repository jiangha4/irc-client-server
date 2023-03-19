FROM python:3.7-bullseye
MAINTAINER Haohan Jiang

EXPOSE 8888

COPY server /usr/src/server

WORKDIR /usr/src/server

CMD ["python", "runner.py"]