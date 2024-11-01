import customtkinter as ctk
from model.password import Password
from view.password_views import FernetHasher

# Configuração inicial do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Senhas")
        self.geometry("400x300")

        # Variável para armazenar a chave temporária
        self.key = None

        # Entrada de chave
        self.label_key = ctk.CTkLabel(self, text="Chave de Criptografia:")
        self.label_key.pack(pady=10)
        self.entry_key = ctk.CTkEntry(self, width=250, show="*")
        self.entry_key.pack(pady=10)

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

    def save_password(self):
        """Função para salvar a senha criptografada para um domínio especificado."""
        key = self.entry_key.get()
        domain = self.entry_domain.get()
        password = self.entry_password.get()

        try:
            fernet = FernetHasher(key)
            encrypted_password = fernet.encrypt(password).decode('utf-8')
            p1 = Password(domain=domain, password=encrypted_password)
            p1.save()
            self.result_label.configure(text="Senha salva com sucesso!")
        except ValueError as e:
            self.result_label.configure(text=f"Erro ao salvar senha: {e}")

    def retrieve_password(self):
        """Função para recuperar e descriptografar a senha para um domínio especificado."""
        key = self.entry_key.get()
        domain = self.entry_domain.get()

        try:
            fernet = FernetHasher(key)
            data = Password.get()
            password = None

            for item in data:
                if domain in item['domain']:
                    password = fernet.decrypt(item['password'])
                    break

            if password:
                self.result_label.configure(text=f"Senha recuperada: {password}")
            else:
                self.result_label.configure(text="Nenhuma senha encontrada para este domínio.")
        except ValueError as e:
            self.result_label.configure(text=f"Erro ao recuperar senha: {e}")


# Execução da aplicação
if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
