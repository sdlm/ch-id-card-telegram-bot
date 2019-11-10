FROM python:3.7
ENV APP_HOME="/app"
WORKDIR ${APP_HOME}

RUN pip install poetry
COPY poetry.lock ./
COPY pyproject.toml ./
RUN poetry config settings.virtualenvs.create false && \
    poetry install --no-dev --no-ansi --no-interaction
