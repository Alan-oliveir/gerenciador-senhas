from datetime import datetime
from pathlib import Path

# Diretório configurável para banco de dados
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / 'db'


class BaseModel:
    """
    Classe base para manipulação de salvamento e recuperação de dados em arquivos de texto.

    Atributos:
        DB_DIR (Path): Diretório onde os arquivos de dados são armazenados.
    """

    def save(self):
        """
        Salva os atributos da instância em um arquivo de texto específico para a classe.

        Cada instância é salva em uma nova linha, com os atributos separados por '|'.
        Levanta:
            IOError: Se ocorrer algum erro ao salvar os dados no arquivo.
        """
        table_path = DB_DIR / f'{self.__class__.__name__}.txt'
        DB_DIR.mkdir(exist_ok=True)  # Cria o diretório do banco de dados, se não existir

        if not table_path.exists():
            table_path.touch()

        try:
            with open(table_path, 'a') as arq:
                arq.write("|".join(list(map(str, self.__dict__.values()))))
                arq.write('\n')
        except IOError as e:
            raise IOError(f"Erro ao salvar os dados no arquivo: {table_path}") from e

    @classmethod
    def get(cls):
        """
        Recupera todas as instâncias salvas da classe a partir de um arquivo de texto.

        Retorna:
            list[dict]: Lista de dicionários, onde cada dicionário representa uma instância com seus atributos.
        Levanta:
            IOError: Se ocorrer algum erro ao ler os dados do arquivo.
        """
        table_path = DB_DIR / f'{cls.__name__}.txt'

        # Garantir que o diretório exista antes de acessar o arquivo
        DB_DIR.mkdir(exist_ok=True)  # Cria o diretório do banco de dados, se não existir

        if not table_path.exists():
            table_path.touch()

        results = []
        atributos = vars(cls()).keys()

        try:
            with open(table_path, 'r') as arq:
                linhas = arq.readlines()
                for linha in linhas:
                    split_values = linha.strip().split('|')
                    tmp_dict = dict(zip(atributos, split_values))
                    results.append(tmp_dict)
        except IOError as e:
            raise IOError(f"Erro ao ler os dados do arquivo: {table_path}") from e

        return results


class Password(BaseModel):
    """
    Classe para representar uma senha e seu domínio associado.

    Atributos:
        domain (str): Domínio associado à senha.
        password (str): A senha criptografada.
        create_at (str): Data e hora da criação da senha.
        expire (int): Indica se a senha expira (1) ou não (0).
    """

    def __init__(self, domain=None, password=None, expire=False):
        """
        Inicializa uma nova instância da classe Password.

        Parâmetros:
            domain (str): Domínio associado à senha.
            password (str): Senha criptografada.
            expire (bool): Indica se a senha expira.
        """
        self.domain = domain
        self.password = password
        self.create_at = datetime.now().isoformat()
        self.expire = 1 if expire else 0
