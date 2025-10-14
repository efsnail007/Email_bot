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

    def get_last_uid_email(self):
        with self.email_client as client:
            return client.get_last_uid_email()

    def get_and_read_last_unseen_emails(self, last_uuid):
        with self.email_client as client:
            unseen_emails = client.get_uid_emails_unseen()
            result = []
            for unseen_uuid in unseen_emails[::-1]:
                if unseen_uuid > last_uuid:
                    from_user, to_user, subject, payload = client.get_email_message(
                        str(unseen_uuid).encode()
                    )
                    result.append((from_user, to_user, subject, payload))
                else:
                    break
            return result
