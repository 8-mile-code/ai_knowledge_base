FROM python:3.12

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync

COPY . .

ENV PYTHONPATH=/app