FROM python:3.9

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
    
# Configure Poetry
ENV POETRY_VERSION=1.3.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}


# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

# Install dependencies
COPY ./py/server/poetry.lock /py/server/pyproject.toml ./
RUN poetry install

# Run your app
COPY ./py/server /app
COPY ./py/server/pyproject.toml /app/pyproject.toml

CMD [ "poetry", "run", "flask", "--app", "server.app", "--debug", "run", "--host", "0.0.0.0", "--port", "5000"]