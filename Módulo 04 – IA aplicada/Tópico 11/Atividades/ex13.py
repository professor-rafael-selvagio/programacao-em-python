# Exercício 13: Crie um jogo de adivinhação com um número secreto entre 1 e
# 20. A função validar_chute() deve converter a entrada com segurança, usando
# try-except e retornando None quando a entrada não for válida. O jogador tem
# 5 tentativas e recebe dicas se o número secreto é maior ou menor.

import random


def validar_chute(entrada):
    try:
        chute = int(entrada)
    except ValueError:
        return None

    if chute < 1 or chute > 20:
        return None

    return chute


numero_secreto = random.randint(1, 20)
tentativas = 0
acertou = False

print("Tente adivinhar o número secreto entre 1 e 20!")

while tentativas < 5:
    entrada = input(f"Tentativa {tentativas + 1} de 5: ")
    chute = validar_chute(entrada)

    if chute is None:
        print("Chute inválido. Digite um número inteiro entre 1 e 20.")
        continue

    tentativas += 1

    if chute == numero_secreto:
        print("Parabéns! Você acertou!")
        acertou = True
        break
    if chute < numero_secreto:
        print("O número secreto é maior.")
    else:
        print("O número secreto é menor.")

if not acertou:
    print(f"Suas tentativas acabaram. O número secreto era {numero_secreto}.")
