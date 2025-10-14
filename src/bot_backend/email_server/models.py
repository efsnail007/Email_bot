"""
Модуль моделей Django для приложения email_server.

Содержит определения моделей, используемых для хранения данных
о пользователях и их почтовых ящиках.
"""

from django.db import models


class User(models.Model):
    """
    Модель пользователя Telegram.
    
    Хранит основную информацию о пользователе бота.
    """
    # Уникальный идентификатор пользователя в Telegram
    tg_id = models.BigIntegerField(
        primary_key=True,
        verbose_name='ID пользователя в Telegram',
        help_text='Уникальный идентификатор пользователя в Telegram'
    )
    
    # Имя пользователя
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        help_text='Имя пользователя'
    )
    
    # Фамилия пользователя (может быть пустой)
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
        help_text='Фамилия пользователя',
        blank=True,
        null=True
    )
    
    class Meta:
        """Метаданные модели пользователя."""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f"{self.first_name} {self.last_name or ''} (ID: {self.tg_id})"


class Email(models.Model):
    """
    Модель почтового ящика.
    
    Связывает почтовый ящик с пользователем и хранит
    информацию о последнем обработанном письме.
    """
    # Email-адрес (уникальный идентификатор)
    email = models.EmailField(
        primary_key=True,
        verbose_name='Email адрес',
        help_text='Адрес электронной почты'
    )
    
    # Зашифрованный пароль от почтового ящика
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        help_text='Зашифрованный пароль от почтового ящика'
    )
    
    # UID последнего обработанного письма
    last_uuid_seen = models.BigIntegerField(
        default=0,
        verbose_name='Последний обработанный UID',
        help_text='UID последнего обработанного письма в этом ящике'
    )
    
    # Связь с пользователем (владельцем почтового ящика)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='emails',
        verbose_name='Пользователь',
        help_text='Владелец почтового ящика'
    )
    
    class Meta:
        """Метаданные модели почтового ящика."""
        verbose_name = 'Почтовый ящик'
        verbose_name_plural = 'Почтовые ящики'
    
    def __str__(self) -> str:
        """Строковое представление почтового ящика."""
        return f"{self.email} (пользователь: {self.user.tg_id})"
