from cryptography.fernet import Fernet
from django.apps import AppConfig

from bot_backend.settings import FERNET_KEY


class EmailServerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "email_server"
    key = FERNET_KEY
    fernet = Fernet(key)
