"""
Настройка Celery для асинхронных и периодических задач.

Этот модуль инициализирует и настраивает экземпляр Celery для работы с Django.
"""

import os

from celery import Celery
from celery.schedules import crontab

# Установка переменной окружения для настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_backend.settings")

# Создание экземпляра приложения Celery
app = Celery("bot_backend")

# Загрузка настроек из настроек Django с префиксом 'CELERY_'
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

# Конфигурация расписания для периодических задач (Celery Beat)
app.conf.beat_schedule = {
    # Задача, которая будет выполняться по расписанию
    "every": {
        # Путь к задаче в формате 'приложение.tasks.имя_функции'
        "task": "email_server.tasks.send_request_bot",
        # Расписание выполнения (в данном случае - каждая минута)
        # crontab() без параметров означает выполнение каждую минуту
        # Для настройки другого расписания можно использовать:
        # - crontab(minute=0, hour=0) - каждый день в полночь
        # - crontab(minute='*/15') - каждые 15 минут
        # - crontab(day_of_week='mon-fri', hour=9, minute=0) - по будням в 9:00
        "schedule": crontab(),
    },
    # Здесь можно добавить другие периодические задачи
}

# Для отладки можно раскомментировать следующую строку, чтобы видеть конфигурацию
# print(f"Celery beat schedule: {app.conf.beat_schedule}")
