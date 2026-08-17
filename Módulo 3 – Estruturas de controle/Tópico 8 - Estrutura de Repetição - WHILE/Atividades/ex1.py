# 1. Senha correta
# Solicite uma senha até que ela esteja correta. Depois, mostre
# a mensagem "Acesso permitido!".

senha_correta = "python123"
senha = input("Digite a senha: ")

while senha != senha_correta:
    senha = input("Senha incorreta. Tente novamente: ")

print("Acesso permitido!")
