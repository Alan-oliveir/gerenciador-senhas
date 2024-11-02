from datetime import datetime
from pathlib import Path

# Diretório configurável para banco de dados
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / 'db'


class BaseModel:
    """Classe base para manipulação de dados em arquivos de texto."""

    def save(self):
        """Salva os atributos da instância em um arquivo específico para a classe."""
        table_path = DB_DIR / f'{self.__class__.__name__}.txt'
        DB_DIR.mkdir(exist_ok=True)  # Garante que o diretório exista

        if not table_path.exists():
            table_path.touch()

        with open(table_path, 'a') as arq:
            arq.write("|".join(list(map(str, self.__dict__.values()))))
            arq.write('\n')

    @classmethod
    def get_all(cls):
        """Recupera todas as instâncias da classe."""
        table_path = DB_DIR / f'{cls.__name__}.txt'
        DB_DIR.mkdir(exist_ok=True)

        if not table_path.exists():
            table_path.touch()

        results = []
        atributos = vars(cls()).keys()

        with open(table_path, 'r') as arq:
            linhas = arq.readlines()
            for linha in linhas:
                split_values = linha.strip().split('|')
                tmp_dict = dict(zip(atributos, split_values))
                results.append(tmp_dict)

        return results


class Password(BaseModel):
    """Classe para representar uma senha e seu domínio associado."""

    def __init__(self, domain=None, password=None, expire=False):
        self.domain = domain
        self.password = password
        self.create_at = datetime.now().isoformat()
        self.expire = 1 if expire else 0

    @classmethod
    def update_password(cls, domain, new_password):
        """Atualiza a senha para um domínio especificado."""
        data = cls.get_all()
        updated_data = []

        for item in data:
            if item['domain'] == domain:
                item['password'] = new_password
            updated_data.append(item)

        # Reescreve o arquivo com os dados atualizados
        cls.save_all(updated_data)

    @classmethod
    def delete_password(cls, domain):
        """Remove a entrada de senha para o domínio especificado."""
        data = cls.get_all()
        updated_data = [item for item in data if item['domain'] != domain]
        cls.save_all(updated_data)

    @classmethod
    def save_all(cls, data):
        """Salva todos os dados fornecidos no arquivo de armazenamento."""
        table_path = DB_DIR / f'{cls.__name__}.txt'
        with open(table_path, 'w') as arq:
            for item in data:
                arq.write("|".join(list(map(str, item.values()))) + '\n')
