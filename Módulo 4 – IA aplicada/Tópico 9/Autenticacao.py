usuario_correto = "admin"
senha_correta = "1234"
senha_admin = "admin123"

tentativas = 0

while tentativas < 3:
    usuario = input("Digite o usuário: ")
    senha = input("Digite a senha: ")

    if usuario == usuario_correto and senha == senha_correta:
        print("Acesso Liberado")
        break
    else:
        tentativas += 1
        print("Usuário ou senha incorretos.")

        if tentativas == 3:
            print("Conta Bloqueada")

            admin = input("Digite a senha do Admin para desbloquear: ")

            if admin == senha_admin:
                tentativas = 0
                print("Conta desbloqueada!")
            else:
                print("Senha de Admin incorreta.")
                break

print("Fim")