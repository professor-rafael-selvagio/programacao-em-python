# Exercício 2: Crie um programa que peça ao usuário para digitar um número
# decimal qualquer. Em seguida, importe a biblioteca math, calcule a raiz
# quadrada desse número e utilize math.ceil para arredondar o resultado para
# o número inteiro mais próximo.

import math


numero = float(input("Digite um número decimal não negativo: ").replace(",", "."))

if numero < 0:
    print("Não é possível calcular a raiz quadrada de um número negativo.")
else:
    raiz = math.sqrt(numero)
    raiz_arredondada = math.ceil(raiz)
    print(f"A raiz quadrada de {numero} é {raiz:.2f}.")
    print(f"Arredondando para cima, o resultado é {raiz_arredondada}.")
