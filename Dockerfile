#syntax=docker/dockerfile:1

FROM python

WORKDIR .

COPY . .

RUN apt-get update -y
RUN apt-get install tk -y


CMD [ "python3", "./main.py" ]
