# Используем официальный образ Python 3.13.7
# Базовый образ содержит все необходимое для запуска Python-приложений
FROM python:3.13.7

# Информация о разработчике
MAINTAINER Snail

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/app

# Копируем файл зависимостей в контейнер
COPY pyproject.toml .

# Устанавливаем зависимости проекта
# 1. Устанавливаем poetry (менеджер зависимостей Python)
# 2. Настраиваем poetry для установки пакетов в системный Python
# 3. Устанавливаем зависимости без dev-зависимостей
RUN python -m pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi

# Копируем исходный код приложения в контейнер
# Копируется после установки зависимостей для ускорения пересборки
COPY src/bot_backend .