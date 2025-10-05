from cryptography.fernet import Fernet


def encode_password(fernet: Fernet, password: str) -> str:
    """
    Encode a password using the given Fernet key.

    Parameters:
    fernet (Fernet): The Fernet key to use for encoding.
    password (str): The password to encode.

    Returns:
    str: The encoded password.

    """
    return fernet.encrypt(password.encode()).decode()


def decode_password(fernet: Fernet, password: str) -> str:
    """
    Decode a password using the given Fernet key.

    Parameters:
    fernet (Fernet): The Fernet key to use for decoding.
    password (str): The password to decode.

    Returns:
    str: The decoded password.

    """
    return fernet.decrypt(password.encode()).decode()
