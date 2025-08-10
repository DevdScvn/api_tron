FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y netcat-traditional

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

COPY ../poetry.lock poetry.lock
COPY ../pyproject.toml pyproject.toml

RUN poetry install --no-root

COPY . .

CMD ["pytest"]