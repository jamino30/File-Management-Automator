# Latest version of Python
FROM python:latest

# Download Package Information
RUN apt-get update -y

# Install Tkinter
RUN apt-get install tk -y

# Commands to run Tkinter application
CMD [ "python3", "./main.py"]
