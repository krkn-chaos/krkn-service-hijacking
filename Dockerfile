# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /python-docker
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN apt-get update && apt-get install -y curl
RUN pip3 install poetry
RUN poetry install

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]