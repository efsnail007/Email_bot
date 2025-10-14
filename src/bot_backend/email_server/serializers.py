"""
Модуль сериализаторов Django REST Framework для приложения email_server.

Содержит классы для преобразования моделей в JSON и обратно,
а также для валидации входящих данных API.
"""

from rest_framework import serializers

from .models import Email, User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    
    Преобразует объекты модели User в JSON и обратно.
    Используется для API-эндпоинтов, связанных с пользователями.
    """
    
    class Meta:
        """Метаданные сериализатора User."""
        # Указываем модель, с которой работает сериализатор
        model = User
        # Включаем все поля модели в сериализацию
        fields = "__all__"
        # Можно добавить дополнительные настройки, например:
        # fields = ('id', 'tg_id', 'first_name', 'last_name')
        # exclude = ('поле_которое_нужно_исключить',)


class EmailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Email.
    
    Преобразует объекты модели Email в JSON и обратно.
    Автоматически скрывает пароль при сериализации (только для записи).
    """
    
    class Meta:
        """Метаданные сериализатора Email."""
        # Указываем модель, с которой работает сериализатор
        model = Email
        # Включаем все поля модели в сериализацию
        fields = "__all__"
        # Дополнительные настройки полей
        extra_kwargs = {
            # Пароль будет доступен только для записи (не отображается при чтении)
            "password": {"write_only": True}
        }

