FROM python:3.13.7
MAINTAINER Snail

WORKDIR /telegram_bot

COPY pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi

COPY src/telegram_bot ./

CMD ["python", "./aiogram_run.py"]