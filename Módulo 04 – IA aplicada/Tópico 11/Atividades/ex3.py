# Exercício 3: Faça um programa que crie uma lista com cinco nomes inseridos
# por um laço. Após preencher a lista, importe random, embaralhe os nomes e
# escolha aleatoriamente um deles para ser o "monitor" do dia, imprimindo o
# sorteado.

import random


nomes = []

for indice in range(5):
    nome = input(f"Digite o {indice + 1}º nome: ")
    nomes.append(nome)

random.shuffle(nomes)
monitor = random.choice(nomes)

print(f"O monitor do dia será: {monitor}!")
