"""
Модуль для работы с электронной почтой через IMAP.

Содержит классы для подключения к почтовым серверам и работы с письмами.
"""

import email
import imaplib
from abc import ABC, abstractmethod
from typing import Tuple, Optional, List


class BaseEmailClient(ABC):
    """
    Абстрактный базовый класс для работы с электронной почтой.
    Определяет общий интерфейс для всех клиентов электронной почты.
    """
    
    @abstractmethod
    def __init__(self, login: str, password: str, email_server: str):
        """
        Инициализация клиента электронной почты.
        
        Args:
            login: Логин (email) пользователя
            password: Пароль от почтового ящика
            email_server: Адрес IMAP-сервера (опционально)
        """
        pass

    @abstractmethod
    def get_last_uid_email(self) -> int:
        """
        Получает UID последнего письма в ящике.
        
        Returns:
            int: UID последнего письма
        """
        pass

    @abstractmethod
    def get_uid_emails_unseen(self) -> List[int]:
        """
        Получает список UID непрочитанных писем.
        
        Returns:
            List[int]: Список UID непрочитанных писем
        """
        pass

    @abstractmethod
    def get_email_message(self, uid: int) -> Tuple[str, str, str, str]:
        """
        Получает содержимое письма по его UID.
        
        Args:
            uid: UID письма
            
        Returns:
            Кортеж вида (отправитель, получатель, тема, текст письма)
        """
        pass

    @abstractmethod
    def __enter__(self):
        """Контекстный менеджер для использования с оператором with."""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Завершение работы с почтовым клиентом."""
        pass


class ImapClient(BaseEmailClient):
    """
    Реализация клиента для работы с почтой через протокол IMAP.
    Поддерживает SSL-шифрование соединения.
    """
    
    def __init__(self, login: str, password: str, email_server: str = ""):
        """
        Инициализация IMAP клиента.
        
        Args:
            login: Email пользователя
            password: Пароль от почтового ящика
            email_server: Адрес IMAP-сервера (если не указан, формируется из домена email)
        """
        self.username = login
        self.password = password
        self.imap_server = email_server if email_server else f"imap.{login.split('@')[1]}"
        self.imap: Optional[imaplib.IMAP4_SSL] = None

    def get_last_uid_email(self) -> int:
        """
        Получает UID последнего письма в ящике.
        
        Returns:
            int: UID последнего письма
            
        Raises:
            Exception: Если произошла ошибка при получении UID
        """
        result, data = self.imap.uid("search", None, "ALL")
        latest_email_uid = data[0].split()[-1]
        return int(latest_email_uid.decode())

    def get_uid_emails_unseen(self) -> List[int]:
        """
        Получает список UID непрочитанных писем.
        
        Returns:
            List[int]: Список UID непрочитанных писем
            
        Raises:
            Exception: Если произошла ошибка при получении списка писем
        """
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
    def get_first_text_block(email_message_instance) -> str:
        """
        Извлекает текстовую часть из письма.
        
        Args:
            email_message_instance: Объект сообщения email
            
        Returns:
            str: Текстовая часть письма или строка "None", если не найдена
        """
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
        """
        Вспомогательный метод для преобразования байтов в целое число.
        
        Args:
            x: Байтовая строка с числом
            
        Returns:
            int: Преобразованное число
        """
        return int(x.decode())

    def __enter__(self) -> 'ImapClient':
        """
        Устанавливает соединение с почтовым сервером при входе в контекстный менеджер.
        
        Returns:
            ImapClient: Текущий экземпляр класса
            
        Raises:
            Exception: Если не удалось подключиться к серверу
        """
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_server)
            self.imap.login(self.username, self.password)
            self.imap.select("INBOX")
            return self
        except Exception as e:
            raise Exception(f"Ошибка подключения к почтовому серверу: {str(e)}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрывает соединение с почтовым сервером при выходе из контекстного менеджера.
        """
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except Exception:
                # Игнорируем ошибки при закрытии соединения
                pass
