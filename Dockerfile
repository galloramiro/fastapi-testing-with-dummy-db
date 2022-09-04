FROM python:3.9.12 as release-base

WORKDIR /app

RUN pip install --user poetry==1.1.14
ENV PATH="/root/.local/bin:${PATH}"

#COPY poetry.lock /app/
COPY pyproject.toml /app/
RUN poetry lock
RUN poetry install --no-dev

# Release
FROM release-base as release
COPY docker-entrypoint.sh /
COPY bin /app/bin
COPY migrations /app/migrations
COPY alembic.ini /app/alembic.ini
COPY src /app/src

# Testing
FROM release-base as test
RUN poetry install
COPY src /app/src

CMD poetry run newrelic-admin run-program gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000 src.main:app --workers=3