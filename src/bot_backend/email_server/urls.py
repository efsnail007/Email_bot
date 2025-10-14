"""
URL-конфигурация для API приложения email_server.

Определяет маршруты (эндпоинты) API для работы с пользователями и их почтовыми ящиками.
Все URL-адреса имеют префикс /api/, который определен в корневом urls.py.
"""

from django.urls import path

from .views import EmailAPI, EmailDetailAPI, UserAPI, UserDetailAPI

# Шаблоны URL для API
urlpatterns = [
    # Создание нового пользователя
    path(
        "user/",
        UserAPI.as_view(),
        name="user_set",
    ),
    
    # Получение, обновление или удаление пользователя по его tg_id
    path(
        "user/<int:tg_id>/",
        UserDetailAPI.as_view(),
        name="user_detail",
    ),
    
    # Получение списка почтовых ящиков пользователя или создание нового
    path(
        "user/<int:tg_id>/email/",
        EmailAPI.as_view(),
        name="email",
    ),
    
    # Получение, обновление или удаление конкретного почтового ящика
    path(
        "user/<int:tg_id>/email/<str:pk>/",
        EmailDetailAPI.as_view(),
        name="email_detail",
    ),
]

# Примеры запросов к API:
#
# 1. Создание пользователя:
#    POST /api/user/ {"tg_id": 123456789, "first_name": "Иван", "last_name": "Иванов"}
#
# 2. Получение информации о пользователе:
#    GET /api/user/123456789/
#
# 3. Добавление почтового ящика пользователю:
#    POST /api/user/123456789/email/ {"email": "example@mail.com", "password": "securepassword"}
#
# 4. Получение списка почтовых ящиков пользователя:
#    GET /api/user/123456789/email/
#
# 5. Удаление почтового ящика:
#    DELETE /api/user/123456789/email/example@mail.com/
