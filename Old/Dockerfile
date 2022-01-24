FROM python:3.9.1-slim-buster
LABEL maintainer="Fabian Wilhelm"
WORKDIR /app/
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt 
EXPOSE 5000
ENTRYPOINT [ "gunicorn" , "-w 4", "-b 0.0.0.0:5000", "mobileFlask:app" ]
