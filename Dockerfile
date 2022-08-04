#syntax=docker/dockerfile:1

# latest version of python
FROM python

WORKDIR .
COPY . .

# update and install Tkinter
RUN apt-get update -y && \
  apt-get install tk -y

# Run main file
CMD [ "python3", "./main.py" ]
