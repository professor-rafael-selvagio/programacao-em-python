# 1. Senha correta
# Solicite uma senha até que ela esteja correta. Depois, mostre
# a mensagem "Acesso permitido!".

senha_correta = "python123"
senha_digitada = ""
tentativas = 0

while senha_digitada != senha_correta and tentativas < 3:
    senha_digitada = input("Senha incorreta. Tente novamente: ")
    tentativas += 1

if senha_digitada == senha_correta:
    print("Acesso permitido!")
else:
    print("Número máximo de tentativas excedido. Acesso negado.")
