import customtkinter as ctk
from .models import Password
from .encryption import FernetHasher
from .dialogs import ErrorWindow

# Configuração inicial do customtkinter
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


def prompt_key():
    """
    Abre um diálogo para solicitar a chave de criptografia ao usuário.

    Retorna:
        str: A chave de criptografia fornecida pelo usuário ou None se cancelar.
    """
    dialog = ctk.CTkInputDialog(text="Digite sua chave de criptografia:", title="Autenticação")
    key = dialog.get_input()

    # Se o usuário pressionar "Cancelar", retorna None
    if key == "" or key is None:
        return None
    return key


class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Senhas")
        self.geometry("400x370")

        # Solicita a chave ao usuário ao iniciar
        self.key = prompt_key()

        # Caso o usuário tenha cancelado o input, fecha a aplicação
        if not self.key:
            self.destroy()
            return

        # Entrada de domínio
        self.label_domain = ctk.CTkLabel(self, text="Domínio:")
        self.label_domain.pack(pady=10)
        self.entry_domain = ctk.CTkEntry(self, width=250)
        self.entry_domain.pack(pady=10)

        # Entrada de senha (somente para salvar)
        self.label_password = ctk.CTkLabel(self, text="Senha:")
        self.label_password.pack(pady=10)
        self.entry_password = ctk.CTkEntry(self, width=250, show="*")
        self.entry_password.pack(pady=10)

        # Botões de salvar e recuperar
        self.save_button = ctk.CTkButton(self, text="Salvar Senha", command=self.save_password)
        self.save_button.pack(pady=10)
        self.retrieve_button = ctk.CTkButton(self, text="Recuperar Senha", command=self.retrieve_password)
        self.retrieve_button.pack(pady=10)

        # Área de exibição de senha recuperada
        self.result_label = ctk.CTkLabel(self, text="", wraplength=300)
        self.result_label.pack(pady=20)

    def show_error(self, message):
        """
        Exibe uma janela de erro com a mensagem fornecida.

        Parâmetros:
            message (str): A mensagem de erro a ser exibida.
        """
        ErrorWindow(self, message)

    def save_password(self):
        """Função para salvar a senha criptografada para um domínio especificado."""
        domain = self.entry_domain.get()
        password = self.entry_password.get()

        try:
            fernet = FernetHasher(self.key)
            encrypted_password = fernet.encrypt(password).decode('utf-8')
            p1 = Password(domain=domain, password=encrypted_password)
            p1.save()
            self.result_label.configure(text="Senha salva com sucesso!")
        except ValueError as e:
            self.show_error(f"Erro ao salvar senha: {e}")

    def retrieve_password(self):
        """Função para recuperar e descriptografar a senha para um domínio especificado."""
        domain = self.entry_domain.get()

        try:
            fernet = FernetHasher(self.key)
            data = Password.get_all()
            password = None

            for item in data:
                if domain in item['domain']:
                    password = fernet.decrypt(item['password'])
                    break

            if password:
                self.result_label.configure(text=f"Senha recuperada: {password}")
            else:
                self.show_error("Nenhuma senha encontrada para este domínio.")
        except ValueError as e:
            self.show_error(f"Erro ao recuperar senha: {e}")
