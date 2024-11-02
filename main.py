from app.app import PasswordManagerApp
from app.models import initialize_database

# Inicializa o banco de dados
initialize_database()

# Executa a aplicação
if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
