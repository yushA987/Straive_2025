#FROM python:3.8-slim-buster
#
#WORKDIR /python-flask-docker
#
#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt
#
#COPY . .
#
#EXPOSE 5000
#
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

FROM python:3.8-slim-bookworm

WORKDIR /python-flask-docker

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--app", "app.py"]


