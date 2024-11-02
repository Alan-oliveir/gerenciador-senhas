# Gerenciador de Senhas

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Projeto de um Gerenciador de Senhas desenvolvido em Python com uma interface gráfica utilizando `customtkinter`.
O aplicativo permite armazenar, atualizar, recuperar e deletar senhas de forma segura.
em um banco de dados SQLite, com criptografia para proteger as informações sensíveis.

___

## Funcionalidades

- **Interface Gráfica**: Interface intuitiva com `customtkinter` para facilitar a interação do usuário.
- **Armazenamento Seguro**: As senhas são criptografadas e armazenadas em um banco de dados SQLite.
- **Gerenciamento de Senhas**:
  - **Salvar**: Armazena um novo domínio e senha.
  - **Atualizar**: Atualiza a senha de um domínio já existente.
  - **Recuperar**: Exibe a senha de um domínio.
  - **Deletar**: Remove o registro de um domínio específico.
- **Verificação de Força de Senha**: Ao criar uma nova senha, a aplicação garante que ela atenda aos requisitos de
  segurança (mínimo de 8 caracteres, incluindo letras maiúsculas e minúsculas, números e caracteres especiais).
- **Segurança de Acesso**: O usuário cria uma senha principal que gera uma chave de criptografia única. Esta chave é
  verificada a cada execução do programa para garantir o acesso autorizado.

## Requisitos

- `customtkinter` para interface gráfica
- `sqlite3` para gerenciamento do banco de dados
- `cryptography` para criptografia de senhas

Instale as dependências com:

```bash
pip install customtkinter cryptography
```
___

## Como Usar

- Configuração Inicial: Ao iniciar o aplicativo pela primeira vez, você será solicitado a criar uma senha principal.
  Essa senha gerará uma chave de criptografia para proteger as senhas armazenadas.
  Guarde-a com cuidado, pois ela será necessária para acessar o programa.

- Interface Gráfica:
  - Domínio: Informe o domínio do serviço (ex.: "gmail.com").
  - Senha: Informe a senha para o domínio.
  - Botão Salvar/Atualizar: Salva uma nova senha para o domínio ou, se o domínio já existir, atualiza a senha.
  - Botão Deletar: Remove o domínio e a senha associada do banco de dados.
  - Botão Recuperar: Exibe a senha do domínio especificado (a senha será descriptografada).

- Mensagens de Erro e Confirmação: O programa exibe mensagens informativas
  e de erro para confirmar ações ou informar sobre domínios não encontrados.

## Segurança

- Criptografia: Todas as senhas são criptografadas usando Fernet do módulo cryptography, utilizando uma chave gerada a
  partir da senha principal do usuário.
- Banco de Dados SQLite: As senhas são armazenadas de maneira segura em um banco de dados local, password_manager.db.
- Validação de Senha: O aplicativo verifica a força da senha principal, garantindo que tenha uma combinação de
  caracteres fortes antes de usá-la para gerar uma chave de criptografia.

___

## Screenshot

![screen](https://github.com/Alan-oliveir/gerenciador-senhas/blob/main/assets/screenshot.png)  

___

## Contribuição

Este é um projeto de estudo, mas melhorias e sugestões são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar
um pull request com suas ideias.

## Licença

[![NPM](https://img.shields.io/npm/l/react)](https://github.com/Alan-oliveir/gerenciador-senhas/blob/main/LICENSE.md)  
Este projeto é licenciado sob a licença MIT. Consulte LICENSE para mais informações.

___

## Contato

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alan-ogoncalves)
