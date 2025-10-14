"""
Основной URL-конфигурация для проекта bot_backend.

Этот модуль определяет корневые URL-шаблоны, которые будут использоваться в проекте.
"""

from django.contrib import admin
from django.urls import include, path

# Основные URL-шаблоны проекта
urlpatterns = [
    # Административная панель Django
    # Доступна по адресу: /admin/
    path("admin/", admin.site.urls),
    # Включение URL-ов из приложения email_server
    # Все URL из email_server.urls будут доступны с префиксом /api/
    # Например: /api/...
    path("api/", include("email_server.urls")),
    # Дополнительные маршруты можно добавлять здесь
    # Пример:
    # path('another-app/', include('another_app.urls')),
]
