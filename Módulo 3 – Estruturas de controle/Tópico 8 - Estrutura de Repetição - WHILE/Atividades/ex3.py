# 3 - Solicite uma senha ao usuário, permitindo no máximo 3 tentativas.
# A senha correta é "python123".

senha_correta = "python123"
tentativas = 0
senha = ""

while tentativas < 3 and senha != senha_correta:
    senha = input("Digite a senha: ")
    tentativas += 1

if senha == senha_correta:
    print("Acesso autorizado")
else:
    print("Acesso bloqueado")
