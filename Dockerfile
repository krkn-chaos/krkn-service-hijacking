# syntax=docker/dockerfile:1

FROM registry.fedoraproject.org/f33/python3

WORKDIR /python-docker
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

USER root
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN pip3 install poetry
RUN poetry install

COPY . .

CMD [ "flask", "run", "--host=0.0.0.0"]