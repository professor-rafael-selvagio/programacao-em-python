# Exercício 4: Peça ao usuário para digitar o ano exato em que nasceu.
# Utilize try-except para converter a entrada para inteiro. Se o usuário
# digitar letras, capture o erro e exiba uma mensagem pedindo apenas números.

try:
    ano_nascimento = int(input("Digite o ano em que você nasceu: "))
    print(f"Ano de nascimento informado: {ano_nascimento}")
except ValueError:
    print("Entrada inválida. Digite apenas números para informar o ano.")
