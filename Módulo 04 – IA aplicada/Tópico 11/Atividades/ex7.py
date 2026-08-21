# Exercício 7: Crie uma função verifica_par que receba um inteiro como
# parâmetro e retorne True se for perfeitamente par, ou False caso contrário.
# Teste a função pedindo um número ao usuário.

def verifica_par(numero):
    return numero % 2 == 0


numero = int(input("Digite um número inteiro: "))
print(f"O número é par? {verifica_par(numero)}")
