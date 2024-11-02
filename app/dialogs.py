import customtkinter as ctk


class ErrorWindow(ctk.CTkToplevel):
    """Janela para exibir mensagens de erro."""

    def __init__(self, master, message):
        super().__init__(master)
        self.title("Erro")

        # Exibe a mensagem de erro
        self.label = ctk.CTkLabel(self, text=message, wraplength=350)
        self.label.pack(padx=20, pady=20)

        # Fecha a janela automaticamente após 3 segundos (3000 ms)
        self.after(3000, self.destroy)
