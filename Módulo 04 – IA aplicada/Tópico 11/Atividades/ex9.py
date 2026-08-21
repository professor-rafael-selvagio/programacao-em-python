# Exercício 9: Crie uma função maior_de_tres que receba três números
# distintos e retorne qual deles é o maior valor numérico.

def maior_de_tres(primeiro, segundo, terceiro):
    return max(primeiro, segundo, terceiro)


numero1 = float(input("Digite o primeiro número: ").replace(",", "."))
numero2 = float(input("Digite o segundo número: ").replace(",", "."))
numero3 = float(input("Digite o terceiro número: ").replace(",", "."))

maior = maior_de_tres(numero1, numero2, numero3)
print(f"O maior número é: {maior:g}")
