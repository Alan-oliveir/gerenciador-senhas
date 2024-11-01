import cryptography.fernet


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
