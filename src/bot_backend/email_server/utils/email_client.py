import base64
import email
import imaplib
from abc import ABC, abstractmethod
from email.header import decode_header


class BaseEmailClient(ABC):
    @abstractmethod
    def __init__(self, login: str, password: str, email_server: str):
        pass

    @abstractmethod
    def get_last_uuid_email(self) -> int:
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class ImapClient(BaseEmailClient):
    def __init__(self, login, password, email_server=""):
        self.username = login
        self.password = password
        if email_server:
            self.imap_server = email_server
        else:
            self.imap_server = "imap." + login.split("@")[1]

    def get_last_uuid_email(self) -> int:
        result, data = self.imap.uid("search", None, "ALL")
        latest_email_uid = data[0].split()[-1]
        return int(latest_email_uid.decode())

    def __enter__(self):
        self.imap = imaplib.IMAP4_SSL(self.imap_server)
        self.imap.login(self.username, self.password)
        self.imap.select("INBOX")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.imap.close()
        self.imap.logout()

    # def get_unseen_emails(self):
    #     result, data = self.imap.uid('search', None, "UNSEEN")
    #     return data
    #
    # def get_email(self, uid):
    #     result, data = self.imap.uid('fetch', uid, '(RFC822)')
    #     return data
    #
    # def get_email_message(self, uid):
    #     result, data = self.imap.uid('fetch', uid, '(RFC822)')
    #     raw_email = data[0][1]
    #     return email.message_from_bytes(raw_email)
    #
    # def get_first_text_block(self, email_message_instance):
    #     maintype = email_message_instance.get_content_maintype()
    #     if maintype == 'multipart':
    #         for part in email_message_instance.get_payload():
    #             if part.get_content_maintype() == 'text':
    #                 return part.get_payload()
    #             elif maintype == 'text':
    #                 return email_message_instance.get_payload()


# result, data = imap.uid('search', None, "UNSEEN")
# print(data)
#
# latest_email_uid = data[0].split()[-1]
# x = int(latest_email_uid, 10)
# y = bytes(x)
# print(bin(latest_email_uid))
# print(bin(y))
#
# print(y == latest_email_uid)
#
# result, data = imap.uid('fetch', latest_email_uid, '(RFC822)')
#
# raw_email = data[0][1]
#
#
# email_message = email.message_from_bytes(raw_email)
#
# # print(email.utils.parseaddr(email_message['From'])) # получаем имя отправителя "Yuji Tomita"
# print (email_message.get_payload()[0].get_payload()[0].get_payload()) # Выводит все заголовки.
# #
# def get_first_text_block(email_message_instance):
#     maintype = email_message_instance.get_content_maintype()
#     if maintype == 'multipart':
#         for part in email_message_instance.get_payload():
#             if part.get_content_maintype() == 'text':
#                 return part.get_payload()
#             elif maintype == 'text':
#                 return email_message_instance.get_payload()
