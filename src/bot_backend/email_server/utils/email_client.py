import email
import imaplib
from abc import ABC, abstractmethod


class BaseEmailClient(ABC):
    @abstractmethod
    def __init__(self, login: str, password: str, email_server: str):
        pass

    @abstractmethod
    def get_last_uid_email(self) -> int:
        pass

    @abstractmethod
    def get_uid_emails_unseen(self) -> list[int]:
        pass

    @abstractmethod
    def get_email_message(self, uid):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class ImapClient(BaseEmailClient):
    def __init__(self, login: str, password: str, email_server: str = ""):
        self.username = login
        self.password = password
        if email_server:
            self.imap_server = email_server
        else:
            self.imap_server = "imap." + login.split("@")[1]

    def get_last_uid_email(self) -> int:
        result, data = self.imap.uid("search", None, "ALL")
        latest_email_uid = data[0].split()[-1]
        return int(latest_email_uid.decode())

    def get_uid_emails_unseen(self) -> list[int]:
        result, data = self.imap.uid("search", None, "UNSEEN")
        latest_emails_uid = data[0].split()
        return list(map(self.__int_return, latest_emails_uid))

    def get_email_message(self, uid):
        result, data = self.imap.uid("fetch", uid, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        from_user = email.utils.parseaddr(email_message["From"])
        to_user = email.utils.parseaddr(email_message["TO"])
        subject = email.utils.parseaddr(email_message["Subject"])
        payload = self.get_first_text_block(email_message).replace("\r\n", "")
        return from_user[-1], to_user[-1], subject[-1], payload

    @staticmethod
    def get_first_text_block(email_message_instance):
        maintype = email_message_instance.get_content_maintype()
        if maintype == "multipart":
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == "text":
                    return part.get_payload()
        elif maintype == "text":
            return email_message_instance.get_payload()
        return "None"

    @staticmethod
    def __int_return(x: bytes) -> int:
        return int(x.decode())

    def __enter__(self):
        self.imap = imaplib.IMAP4_SSL(self.imap_server)
        self.imap.login(self.username, self.password)
        self.imap.select("INBOX")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.imap.close()
        self.imap.logout()
