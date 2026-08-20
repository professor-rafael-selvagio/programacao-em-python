# 5. Soma até zero
# Solicite números, acumule a soma e encerre quando o usuário digitar 0.

soma = 0
numero = int(input("Digite um número inteiro (0 para encerrar): "))

while numero != 0:
    soma += numero
    numero = int(input("Digite outro número inteiro (0 para encerrar): "))

print(f"A soma dos números informados é {soma}.")
