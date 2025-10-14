import requests

from bot_backend.celery import app
from bot_backend.settings import BOT_TOKEN

from .apps import EmailServerConfig
from .email_reader import EmailReader
from .models import Email
from .utils.email_client import ImapClient
from .utils.fernet import decode_password


@app.task
def send_request_bot():
    emails = Email.objects.all()
    for email in emails:
        password = decode_password(EmailServerConfig.fernet, email.password)
        client = EmailReader(ImapClient, email.email, password)
        unseen_messages = client.get_and_read_last_unseen_emails(email.last_uuid_seen)
        if unseen_messages:
            for unseen_message in unseen_messages:
                send_message.delay(*unseen_message, email.user.tg_id)
            last_uuid_seen = client.get_last_uid_email()
            email.last_uuid_seen = last_uuid_seen
            email.save()


@app.task
def send_message(from_user, to_user, subject, payload, tg_id):

    message_text = "<b>Новый письмо!</b>\n"
    message_text += f"От кого: {from_user}\n"
    message_text += f"Кому: {to_user}\n"
    message_text += f"Тема: {subject}\n"
    message_text += f"Текст сообщения: {payload}\n"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": tg_id, "text": message_text, "parse_mode": "HTML"}
    requests.post(url, data=data)
