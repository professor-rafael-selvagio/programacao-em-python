import random


def pedir_palpite():
    """Pede um número ao usuário e usa try-except para garantir que a entrada seja válida."""
    while True:
        try:
            # Pede a entrada do usuário e tenta converter para número inteiro
            palpite = int(
                input("Digite o seu palpite (um número entre 1 e 10): ")
            )

            # Opcional: verifica se está dentro do intervalo de 1 a 10
            if 1 <= palpite <= 10:
                return palpite
            else:
                print("⚠️ Por favor, digite um número que esteja ENTRE 1 e 10!")

        except ValueError:
            # Trata o erro caso o usuário digite texto (ex: "cinco", "abc", etc.)
            print(
                "❌ Entrada inválida! Digite apenas números inteiros (ex: 5)."
            )


def jogo_adivinhacao():
    print("=== 🎮 JOGO DE ADIVINHAÇÃO ===\n")

    # 1. Gera um número secreto entre 1 e 10
    numero_secreto = random.randint(1, 10)

    acertou = False
    tentativas = 0

    while not acertou:
        tentativas += 1

        # 2, 3 e 4. Chama a função que pede o palpite seguro
        palpite = pedir_palpite()

        # Valida se o jogador venceu
        if palpite == numero_secreto:
            print(
                f"\n🎉 PARABÉNS! Você acertou o número secreto ({numero_secreto}) em {tentativas} tentativa(s)!"
            )
            acertou = True
        elif palpite < numero_secreto:
            print("💡 Dica: O número secreto é MAIOR.")
        else:
            print("💡 Dica: O número secreto é MENOR.")


# Executa o jogo
if __name__ == "__main__":
    jogo_adivinhacao()