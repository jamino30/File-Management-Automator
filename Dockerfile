# Slim version of Python
FROM python:3.10.5-slim

# Download Package Information
RUN apt-get update -y

# Install Tkinter
RUN apt-get install tk -y

# Commands to run Tkinter application
CMD ["/app/main.py"]
ENTRYPOINT ["python3"]
