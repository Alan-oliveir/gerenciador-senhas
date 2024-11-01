import string
import secrets
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet

class FernetHasher:
    """Classe para manipular criptografia e descriptografia de senhas."""

    RANDOM_STRING_CHARS = string.ascii_letters + string.digits

    def __init__(self, key: str):
        """Inicializa a classe com uma chave de criptografia válida."""
        if not isinstance(key, bytes):
            key = key.encode()
        self.fernet = Fernet(key)

    @classmethod
    def create_key(cls, archive=False):
        """Gera uma nova chave de criptografia e opcionalmente a salva em arquivo."""
        value = cls._get_random_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        key = base64.b64encode(hasher)

        if archive:
            cls._save_key_to_file(key)
        return key

    @classmethod
    def _get_random_string(cls, length=25):
        return ''.join(secrets.choice(cls.RANDOM_STRING_CHARS) for _ in range(length))

    @classmethod
    def _save_key_to_file(cls, key):
        """Salva a chave em um arquivo no diretório de chaves."""
        file_path = Path(__file__).resolve().parent.parent / 'keys' / 'key.key'
        file_path.parent.mkdir(exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(key)

    def encrypt(self, value: str) -> bytes:
        """Criptografa uma string, garantindo que está no formato correto."""
        if not isinstance(value, bytes):
            value = value.encode()
        try:
            return self.fernet.encrypt(value)
        except Exception as e:
            raise ValueError(f"Erro ao criptografar o valor: {e}")

    def decrypt(self, value: bytes) -> str:
        """Descriptografa uma string, garantindo o formato correto e capturando erros."""
        if not isinstance(value, bytes):
            value = value.encode('utf-8')
        try:
            return self.fernet.decrypt(value).decode()
        except Exception as e:
            raise ValueError(f"Erro ao descriptografar o valor: {e}")
