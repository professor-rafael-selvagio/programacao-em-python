# Exercício 10: Desenvolva inverte_texto, que receba uma string e retorne-a
# escrita de trás para frente. Repita até o usuário digitar "sair".

def inverte_texto(texto):
    return texto[::-1]


while True:
    palavra = input("Digite uma palavra (ou 'sair' para encerrar): ")

    if palavra.strip().lower() == "sair":
        print("Programa encerrado.")
        break

    print(f"Texto invertido: {inverte_texto(palavra)}")
