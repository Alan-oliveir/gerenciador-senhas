import string
import secrets
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from typing import Union

# Diretórios configuráveis para arquivos de chaves
BASE_DIR = Path(__file__).resolve().parent.parent
KEY_DIR = BASE_DIR / 'keys'


class FernetHasher:
    """
    Classe para manipular criptografia e descriptografia de senhas usando a biblioteca Fernet.

    Atributos:
        RANDOM_STRING_CHARS (str): Conjunto de caracteres usados para gerar strings aleatórias.
    """

    RANDOM_STRING_CHARS = string.ascii_letters + string.digits

    def __init__(self, key: Union[Path, str]):
        """
        Inicializa um objeto FernetHasher com a chave de criptografia especificada.

        Parâmetros:
            key (Union[Path, str]): Chave usada para instanciar o objeto Fernet.
        Levanta:
            ValueError: Se a chave não estiver no formato correto para a criptografia Fernet.
        """
        try:
            if not isinstance(key, bytes):
                key = key.encode()
            self.fernet = Fernet(key)
        except (TypeError, ValueError) as e:
            raise ValueError("Erro na inicialização da chave. Verifique se ela está corretamente codificada em base64.") from e

    @classmethod
    def _get_random_string(cls, length=25) -> str:
        """
        Gera uma string aleatória com o número de caracteres especificado.

        Parâmetros:
            length (int): Comprimento da string gerada. Padrão é 25.
        Retorna:
            str: String aleatória gerada.
        """
        return ''.join(secrets.choice(cls.RANDOM_STRING_CHARS) for _ in range(length))

    @classmethod
    def create_key(cls, archive=False) -> tuple:
        """
        Cria uma nova chave para criptografia e opcionalmente a salva em arquivo.

        Parâmetros:
            archive (bool): Se verdadeiro, salva a chave em um arquivo. Padrão é False.
        Retorna:
            tuple: Retorna a chave gerada e o caminho do arquivo se a chave for salva.
        """
        value = cls._get_random_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        key = base64.b64encode(hasher)
        if archive:
            return key, cls.archive_key(key)
        return key, None

    @classmethod
    def archive_key(cls, key: bytes) -> Path:
        """
        Salva uma chave de criptografia em um arquivo exclusivo.

        Parâmetros:
            key (bytes): A chave de criptografia a ser salva.
        Retorna:
            Path: Caminho do arquivo onde a chave foi salva.
        """
        KEY_DIR.mkdir(exist_ok=True)  # Cria o diretório se não existir
        file = 'key.key'
        while (KEY_DIR / file).exists():
            file = f'key_{cls._get_random_string(5)}.key'
        file_path = KEY_DIR / file
        try:
            with open(file_path, 'wb') as arq:
                arq.write(key)
        except IOError as e:
            raise IOError(f"Erro ao salvar a chave no arquivo: {file_path}") from e
        return file_path

    def encrypt(self, value: str) -> bytes:
        """
        Criptografa uma string usando a chave Fernet.

        Parâmetros:
            value (str): Texto a ser criptografado.
        Retorna:
            bytes: Texto criptografado em bytes.
        """
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.encrypt(value)

    def decrypt(self, value: bytes) -> str:
        """
        Descriptografa uma string usando a chave Fernet.

        Parâmetros:
            value (bytes): Texto criptografado em bytes.
        Retorna:
            str: Texto descriptografado.
        Levanta:
            InvalidToken: Se o token fornecido não puder ser validado pela chave Fernet.
        """
        if not isinstance(value, bytes):
            value = value.encode('utf-8')
        try:
            return self.fernet.decrypt(value).decode()
        except InvalidToken:
            return 'Token inválido: a chave fornecida não é compatível com o valor criptografado.'
