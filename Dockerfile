from python:3

MAINTAINER Thalida Noel "hello@thalida.com"

COPY . /server
WORKDIR /server

RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["python", "server.py"]
