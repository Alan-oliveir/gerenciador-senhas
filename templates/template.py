import sys
import os
from model.password import Password
from view.password_views import FernetHasher

# Adiciona o diretório atual ao caminho para garantir que os módulos sejam encontrados
sys.path.append(os.path.abspath(os.curdir))


def main():
    """
    Função principal para interação com o usuário, permitindo salvar uma nova senha ou recuperar uma senha existente.
    """
    action = input('Digite 1 para salvar uma nova senha ou 2 para ver uma determinada senha: ')

    match action:
        case '1':
            save_password()
        case '2':
            retrieve_password()
        case _:
            print("Opção inválida. Por favor, escolha 1 ou 2.")


def save_password():
    """
    Salva uma nova senha para um domínio especificado. Gera uma chave de criptografia se for o primeiro uso.
    """
    # Verifica se há senhas salvas. Se não, cria uma nova chave.
    if len(Password.get()) == 0:
        key, path = FernetHasher.create_key(archive=True)
        print('Sua chave foi criada. Salve-a com cuidado; se for perdida, não poderá recuperar suas senhas.')
        print(f'Chave: {key.decode("utf-8")}')
        if path:
            print('Chave salva no arquivo. Remova-o do local original após transferi-lo com segurança.')
            print(f'Caminho: {path}')
    else:
        # Pede a chave existente se já houver senhas salvas
        key = input('Digite sua chave usada para criptografia (use sempre a mesma chave): ')

    domain = input('Domínio: ')
    password = input('Digite a senha: ')
    try:
        fernet = FernetHasher(key)
        encrypted_password = fernet.encrypt(password).decode('utf-8')
        p1 = Password(domain=domain, password=encrypted_password)
        p1.save()
        print("Senha salva com sucesso.")
    except ValueError as e:
        print(f"Erro na criptografia: {e}")


def retrieve_password():
    """
    Recupera uma senha salva para um domínio especificado, descriptografando-a com a chave fornecida pelo usuário.
    """
    domain = input('Domínio: ')
    key = input('Digite sua chave de criptografia: ')

    try:
        fernet = FernetHasher(key)
        data = Password.get()
        password = ''

        for item in data:
            if domain in item['domain']:
                password = fernet.decrypt(item['password'])

        if password:
            print(f'Sua senha: {password}')
        else:
            print('Nenhuma senha encontrada para esse domínio.')
    except ValueError as e:
        print(f"Erro na descriptografia: {e}")


if __name__ == '__main__':
    main()
