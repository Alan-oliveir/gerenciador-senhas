import customtkinter as ctk

from .dialogs import ErrorWindow
from .encryption import validate_password, generate_key_from_password, load_existing_key, FernetHasher
from .models import Password

# Configuração inicial do customtkinter
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Senhas")
        self.geometry("400x420")

        # Solicita a chave ao usuário ao iniciar
        self.key = self.verify_or_create_key()

        # Caso o usuário tenha cancelado o input, fecha a aplicação
        if not self.key:
            self.destroy()
            return

        # Entrada de domínio
        self.label_domain = ctk.CTkLabel(self, text="Domínio:")
        self.label_domain.pack(pady=10)
        self.entry_domain = ctk.CTkEntry(self, width=250)
        self.entry_domain.pack(pady=10)

        # Entrada de senha
        self.label_password = ctk.CTkLabel(self, text="Senha:")
        self.label_password.pack(pady=10)
        self.entry_password = ctk.CTkEntry(self, width=250, show="*")
        self.entry_password.pack(pady=10)

        # Botão para salvar ou atualizar a senha
        self.save_button = ctk.CTkButton(self, text="Salvar/Atualizar Senha", command=self.save_or_update_password)
        self.save_button.pack(pady=10)

        # Botão para deletar a senha de um domínio
        self.delete_button = ctk.CTkButton(self, text="Deletar Senha", command=self.delete_password)
        self.delete_button.pack(pady=10)

        # Botão para recuperar a senha
        self.retrieve_button = ctk.CTkButton(self, text="Recuperar Senha", command=self.retrieve_password)
        self.retrieve_button.pack(pady=10)

        # Área de exibição de senha recuperada ou mensagens
        self.result_label = ctk.CTkLabel(self, text="", wraplength=300)
        self.result_label.pack(pady=20)

    def result_error(self, message):
        """Exibe uma mensagem de erro."""
        self.result_label.configure(text=message, text_color="red")

    def result_info(self, message):
        """Exibe uma mensagem informativa."""
        self.result_label.configure(text=message, text_color="green")

    def save_or_update_password(self):
        """Salva ou atualiza a senha para o domínio especificado."""
        domain = self.entry_domain.get().strip()
        password = self.entry_password.get().strip()

        if not domain or not password:
            self.result_error("Por favor, insira o domínio e a senha.")
            return

        fernet = FernetHasher(self.key)
        encrypted_password = fernet.encrypt(password).decode('utf-8')

        # Verifica se o domínio já existe
        existing_domains = [item['domain'] for item in Password.get_all()]
        if domain in existing_domains:
            # Atualiza a senha existente
            Password.update_password(domain, encrypted_password)
            self.result_info(f"Senha para '{domain}' atualizada com sucesso.")
        else:
            # Salva um novo domínio e senha
            new_password = Password(domain=domain, password=encrypted_password)
            new_password.save()
            self.result_info(f"Senha para '{domain}' salva com sucesso.")

    def delete_password(self):
        """Deleta a senha para o domínio especificado."""
        domain = self.entry_domain.get().strip()

        if not domain:
            self.result_error("Por favor, insira o domínio para deletar.")
            return

        # Verifica se o domínio existe antes de tentar deletar
        existing_domains = [item['domain'] for item in Password.get_all()]
        if domain in existing_domains:
            Password.delete_password(domain)
            self.result_info(f"Senha para '{domain}' deletada com sucesso.")
        else:
            self.result_error(f"Domínio '{domain}' não encontrado.")

    def retrieve_password(self):
        """Recupera e descriptografa a senha para um domínio especificado."""
        domain = self.entry_domain.get().strip()

        if not domain:
            self.result_error("Por favor, insira o domínio para recuperar a senha.")
            return

        try:
            fernet = FernetHasher(self.key)
            data = Password.get_all()
            password = None

            for item in data:
                if domain == item['domain']:
                    password = fernet.decrypt(item['password'])
                    break

            if password:
                self.result_info(f"Senha recuperada: {password}")
            else:
                self.result_error(f"Domínio '{domain}' não encontrado.")
        except ValueError as e:
            self.result_error(f"Erro ao recuperar senha: {e}")

    def show_error(self, message):
        """
        Exibe uma janela de erro com a mensagem fornecida.

        Parâmetros:
            message (str): A mensagem de erro a ser exibida.
        """
        ErrorWindow(self, message)

    def verify_or_create_key(self):
        """
        Verifica se a chave existe, caso contrário pede ao usuário para criar uma senha.

        Retorna:
            bytes: A chave de criptografia gerada ou carregada.
        """
        existing_key = load_existing_key()

        if existing_key:
            attempts = 0  # Contador de tentativas
            while attempts < 3:
                dialog = ctk.CTkInputDialog(text="Digite sua senha para acessar:", title="Autenticação")
                password = dialog.get_input()

                # Se o usuário cancelar ou não digitar nada, encerra a aplicaçao
                if not password:
                    self.destroy()
                    return None

                # Converte a senha para uma chave e verifica se bate com a existente
                generated_key = generate_key_from_password(password)
                if generated_key == existing_key:
                    return generated_key
                else:
                    attempts += 1
                    self.show_error(f"Senha incorreta. Tentativas restantes: {3 - attempts}")

            self.destroy()
            return None

        else:
            # Solicita ao usuário uma nova senha que atende aos requisitos
            while True:
                dialog = ctk.CTkInputDialog(text="Crie uma senha segura:", title="Criar Senha")
                new_password = dialog.get_input()

                # Se o usuário cancelar ou não digitar nada, encerra a aplicaçao
                if not new_password:
                    self.destroy()
                    return None

                if validate_password(new_password):
                    return generate_key_from_password(new_password)
                else:
                    self.show_error(
                        "A senha deve ter pelo menos 8 caracteres, 1 letra maiúscula, 1 minúscula, 1 número e 1 caractere especial."
                    )
