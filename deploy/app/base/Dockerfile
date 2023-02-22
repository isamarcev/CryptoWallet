FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/src

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # curl
  curl


# tzdata for timzone
RUN apt-get update -y
RUN apt-get install -y tzdata

# timezone env with default
ENV TZ=Europe/Kiev

# Upgrade pip
RUN pip install --upgrade pip
RUN pip install setuptools

WORKDIR $PYTHONPATH

COPY ./base_api/poetry.lock ./
COPY ./base_api/pyproject.toml ./


#WORKDIR /usr/src/base_api

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python
ENV PATH "/root/.local/bin:$PATH"


RUN poetry config virtualenvs.in-project true --local
RUN poetry install --no-root --only main --no-interaction --no-ansi

#WORKDIR /usr/src
COPY base_api /usr/src/base_api
COPY services /usr/src/services
COPY logger_config.json /usr/src/logger_config.json
COPY Makefile /usr/src/Makefile
