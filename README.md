# Gerenciador de Senhas

Um aplicativo em Python para gerenciar e armazenar senhas criptografadas localmente. O sistema permite salvar novas senhas e recuperar senhas já armazenadas para diferentes domínios, com um mecanismo de criptografia para proteger os dados.

## Funcionalidades

- **Criptografia**: Usa a biblioteca `cryptography` para criptografar e descriptografar senhas.
- **Armazenamento seguro**: Senhas e domínios são salvos em um arquivo local, criptografados com uma chave segura.
- **Geração de chave criptográfica**: Permite criar uma chave única para criptografar senhas e armazená-la em um arquivo para uso futuro.
- **Interface de linha de comando**: O usuário pode salvar uma nova senha ou visualizar senhas salvas para um domínio específico.

## Pré-requisitos

- Python 3.10+
- Biblioteca `cryptography`

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/gerenciador-senhas.git
   cd gerenciador-senhas
   ```

2. Crie um ambiente virtual:
- Linux:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- Windows:
  ```bash
  python -m venv venv
  venv\Scripts\Activate
  ```

3. Instale as dependencias

## Utilizaçao
1. Inicie o programa
2. Siga as instruções para:
- Salvar uma nova senha (opção 1): Caso seja o primeiro uso, uma nova chave de criptografia será gerada e exibida. Guarde-a com segurança, pois ela será necessária para descriptografar as senhas no futuro.
- Recuperar uma senha existente (opção 2): Informe o domínio e a chave para descriptografar a senha armazenada.

## Estrutura do Projeto

- model/password.py: Define a estrutura do banco de dados local para armazenar senhas.
- view/password_views.py: Lida com a criptografia de senhas usando o FernetHasher.
- template.py: Arquivo principal que gerencia a interação com o usuário e manipula o fluxo de salvar e recuperar senhas.

## Licença
Este projeto é licenciado sob a licença MIT.
