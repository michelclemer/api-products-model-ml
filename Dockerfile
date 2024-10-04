FROM ubuntu:latest
LABEL authors="Michel"
FROM python:3.11
COPY . .
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
