from .utils.email_client import BaseEmailClient, ImapClient


class EmailReader:
    def __init__(
        self,
        email_client: BaseEmailClient,
        login: str,
        password: str,
        email_server: str = "",
    ):
        self.email_client = email_client(login, password, email_server)

    def get_last_uuid_email(self):
        with self.email_client as client:
            return client.get_last_uuid_email()


# password = "jycutrgegrlhajor"
# username = "zresku@yandex.ru"
# print(EmailReader(ImapClient, username, password).get_last_uuid_email())
