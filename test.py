from cryptography.fernet import Fernet
from decouple import AutoConfig
config = AutoConfig()

key = config("FERNET_KEY")

fernet = Fernet(key)

x = fernet.encrypt("password".encode()).decode()
fernet.decrypt(x.encode()).decode()