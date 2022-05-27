FROM python:3.10-slim-buster

WORKDIR /python-docker

RUN pip3 install poetry
COPY . .

RUN poetry install

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
