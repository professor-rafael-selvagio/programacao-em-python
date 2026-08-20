# 4. Digite 0 para sair
# Solicite continuamente números inteiros até que o usuário informe 0.

numero = int(input("Digite um número inteiro (0 para sair): "))

while numero != 0:
    numero = int(input("Digite outro número inteiro (0 para sair): "))

print("Programa encerrado.")
