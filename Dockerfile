FROM python:3.9

WORKDIR /web

RUN apt-get update

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /web

CMD [ "python", "./App/Server.py"]