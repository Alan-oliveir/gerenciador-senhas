import sqlite3
from datetime import datetime
from pathlib import Path

# Caminho para o banco de dados
DB_PATH = Path(__file__).resolve().parent.parent / 'db' / 'password_manager.db'


# Função para conectar ao banco de dados
def get_connection():
    return sqlite3.connect(DB_PATH)


# Criação da tabela
def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expire INTEGER DEFAULT 0
            )
        ''')
        conn.commit()


class BaseModel:
    """Classe base para manipulação de dados no banco de dados."""

    def save(self):
        """Salva a senha e o domínio no banco de dados."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO passwords (domain, password, created_at, expire)
                VALUES (?, ?, ?, ?)
            ''', (self.domain, self.password, self.created_at, self.expire))
            conn.commit()

    @classmethod
    def get_all(cls):
        """Recupera todas as senhas e domínios armazenados no banco de dados."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT domain, password, created_at, expire FROM passwords')
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'domain': row[0],
                    'password': row[1],
                    'created_at': row[2],
                    'expire': row[3]
                })
            return results


class Password(BaseModel):
    """Classe para representar uma senha e seu domínio associado."""

    def __init__(self, domain=None, password=None, expire=False):
        self.domain = domain
        self.password = password
        self.created_at = datetime.now().isoformat()
        self.expire = 1 if expire else 0

    @classmethod
    def update_password(cls, domain, new_password):
        """Atualiza a senha para um domínio especificado no banco de dados."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE passwords
                SET password = ?
                WHERE domain = ?
            ''', (new_password, domain))
            conn.commit()

    @classmethod
    def delete_password(cls, domain):
        """Remove a entrada de senha para o domínio especificado no banco de dados."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM passwords
                WHERE domain = ?
            ''', (domain,))
            conn.commit()
