# 2 - Solicite números inteiros ao usuário até que ele digite 0.
# Ao final, mostre a soma dos números informados, sem incluir o zero.

soma = 0
numero = int(input("Digite um número inteiro (0 para encerrar): "))

while numero != 0:
    soma += numero
    numero = int(input("Digite outro número inteiro (0 para encerrar): "))

print(f"A soma dos números informados é {soma}.")
