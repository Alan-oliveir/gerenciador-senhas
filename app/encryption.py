from base64 import urlsafe_b64encode
from hashlib import sha256
from pathlib import Path

import cryptography.fernet
from password_strength import PasswordPolicy

KEY_DIR = Path(__file__).resolve().parent.parent / 'keys'
KEY_FILE = KEY_DIR / 'key.key'

# Define a política de senha
policy = PasswordPolicy.from_names(
    length=8,  # Pelo menos 8 caracteres
    uppercase=1,  # Pelo menos uma letra maiúscula
    numbers=1,  # Pelo menos um número
    special=1,  # Pelo menos um caractere especial
    nonletters=0  # Pelo menos uma letra
)


def validate_password(password):
    """
        Valida a força da senha com base na política definida.

        Parâmetros:
            password (str): A senha a ser validada.

        Retorna:
            bool: True se a senha atender à política de segurança, False caso contrário.
        """
    # Verifica se a senha atende à política
    errors = policy.test(password)
    return len(errors) == 0


def generate_key_from_password(password):
    """
    Gera uma chave de criptografia a partir de uma senha segura e a salva em um arquivo.

    Parâmetros:
        password (str): A senha a ser usada para criar a chave.
    """
    if not KEY_DIR.exists():
        KEY_DIR.mkdir(parents=True)

    hasher = sha256(password.encode())
    key = urlsafe_b64encode(hasher.digest())

    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key


def load_existing_key():
    """
    Carrega a chave de criptografia se já existir.

    Retorna:
        bytes ou None: A chave se existir, caso contrário None.
    """
    if KEY_FILE.exists():
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    return None


class FernetHasher:
    """Classe para manipular criptografia e descriptografia de senhas."""

    def __init__(self, key: str):
        """Inicializa a classe com uma chave de criptografia válida."""
        if not isinstance(key, bytes):
            key = key.encode()
        self.fernet = cryptography.fernet.Fernet(key)

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
