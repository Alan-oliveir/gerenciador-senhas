import customtkinter as ctk

class ErrorWindow(ctk.CTkToplevel):
    """Janela para exibir mensagens de erro."""

    def __init__(self, master, message):
        super().__init__(master)
        self.title("Erro")

        # Exibe a mensagem de erro
        self.label = ctk.CTkLabel(self, text=message, wraplength=350)
        self.label.pack(padx=20, pady=20)

        # Botão para fechar a janela de erro
        self.close_button = ctk.CTkButton(self, text="Fechar", command=self.destroy)
        self.close_button.pack(pady=(10, 30))

        # Fecha a janela automaticamente após 5 segundos (5000 ms)
        self.after(5000, self.destroy)