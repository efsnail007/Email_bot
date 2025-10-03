# import imaplib
# import email
# from email.header import decode_header
# import base64
# # from bs4 import BeautifulSoup
#
# mail_pass = "jycutrgegrlhajor"
# username = "zresku@yandex.ru"
# imap_server = "imap.yandex.ru"
# imap = imaplib.IMAP4_SSL(imap_server)
# imap.login(username, mail_pass)
# imap.select("INBOX")
#
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
