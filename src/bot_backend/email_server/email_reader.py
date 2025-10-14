"""
Модуль для чтения и обработки электронных писем.

Содержит класс EmailReader, который предоставляет удобный интерфейс
для работы с почтовым клиентом и получения непрочитанных писем.
"""

from typing import List, Tuple, Type, Any

from .utils.email_client import BaseEmailClient, ImapClient


class EmailReader:
    """
    Класс для чтения и обработки электронных писем.
    
    Позволяет получать информацию о последних непрочитанных письмах
    и их содержимое, используя переданный почтовый клиент.
    """
    
    def __init__(
        self,
        email_client: Type[BaseEmailClient],
        login: str,
        password: str,
        email_server: str = "",
    ) -> None:
        """
        Инициализация EmailReader.
        
        Args:
            email_client: Класс почтового клиента, реализующий BaseEmailClient
            login: Логин (email) для входа в почтовый ящик
            password: Пароль от почтового ящика
            email_server: Адрес IMAP-сервера (опционально)
        """
        self.email_client = email_client(login, password, email_server)

    def get_last_uid_email(self) -> int:
        """
        Получает UID последнего письма в почтовом ящике.
        
        Returns:
            int: UID последнего письма
            
        Пример использования:
            >>> reader = EmailReader(ImapClient, "user@example.com", "password")
            >>> last_uid = reader.get_last_uid_email()
        """
        with self.email_client as client:
            return client.get_last_uid_email()

    def get_and_read_last_unseen_emails(self, last_uuid: int) -> List[Tuple[str, str, str, str]]:
        """
        Получает и читает все непрочитанные письма, начиная с указанного UID.
        
        Args:
            last_uuid: UID последнего обработанного письма
            
        Returns:
            List[Tuple[str, str, str, str]]: Список кортежей с информацией о письмах.
                Каждый кортеж содержит (отправитель, получатель, тема, текст письма)
                
        Пример использования:
            >>> reader = EmailReader(ImapClient, "user@example.com", "password")
            >>> last_processed_uid = 100
            >>> new_emails = reader.get_and_read_last_unseen_emails(last_processed_uid)
            >>> for sender, recipient, subject, body in new_emails:
            ...     print(f"От: {sender}, Тема: {subject}")
        """
        with self.email_client as client:
            # Получаем список UID непрочитанных писем
            unseen_emails = client.get_uid_emails_unseen()
            result = []
            for unseen_uuid in unseen_emails[::-1]:
                if unseen_uuid > last_uuid:
                    # Получаем содержимое письма по его UID
                    from_user, to_user, subject, payload = client.get_email_message(
                        str(unseen_uuid).encode()
                    )
                    result.append((from_user, to_user, subject, payload))
                else:
                    # Прерываем цикл, если дошли до уже обработанных писем
                    break
            return result
