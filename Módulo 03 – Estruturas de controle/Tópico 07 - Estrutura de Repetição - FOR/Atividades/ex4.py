# 4 - Solicite um número ao usuário e mostre a tabuada desse número de 1 a 10.

numero = int(input("Digite um número: "))

for multiplicador in range(1, 11):
    resultado = numero * multiplicador
    print(f"{numero} x {multiplicador} = {resultado}")
