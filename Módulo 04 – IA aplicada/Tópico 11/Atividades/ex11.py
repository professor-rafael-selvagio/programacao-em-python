# Exercício 11: Crie sortear_dado() usando random para retornar um número
# de 1 a 6. Solicite quantas vezes o usuário quer jogar, valide a quantidade
# com try-except e use for para imprimir os resultados.

import random


def sortear_dado():
    return random.randint(1, 6)


try:
    quantidade = int(input("Quantas vezes você quer jogar o dado? "))
    if quantidade <= 0:
        print("Digite uma quantidade inteira maior que zero.")
    else:
        for jogada in range(1, quantidade + 1):
            print(f"Jogada {jogada}: {sortear_dado()}")
except ValueError:
    print("Entrada inválida. Digite uma quantidade inteira.")
