# Exercício 6: Crie uma lista com três nomes de cores cadastradas fixas.
# Peça um índice ao usuário e utilize try-except para tratar índices inválidos
# ou entradas que não sejam numéricas.

cores = ["azul", "verde", "vermelho"]

try:
    indice = int(input("Digite o índice da cor que deseja visualizar (0 a 2): "))
    print(f"A cor escolhida é: {cores[indice]}")
except ValueError:
    print("Entrada inválida. Digite um número inteiro.")
except IndexError:
    print("Índice inválido. Escolha um índice entre 0 e 2.")
