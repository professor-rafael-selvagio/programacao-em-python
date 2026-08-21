# Exercício 1: Escreva um programa que importe a biblioteca random e
# sorteie um número inteiro aleatório entre 1 e 50, imprimindo o resultado
# na tela com uma mensagem amigável para o usuário.

import random


numero_sorteado = random.randint(1, 50)
print(f"O número sorteado foi: {numero_sorteado}!")
