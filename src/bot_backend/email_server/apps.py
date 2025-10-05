from cryptography.fernet import Fernet
from django.apps import AppConfig


class EmailServerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "email_server"
    key = Fernet.generate_key()
    fernet = Fernet(key)
