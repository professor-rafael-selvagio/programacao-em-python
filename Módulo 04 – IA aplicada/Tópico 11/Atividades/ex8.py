# Exercício 8: Escreva uma função calcular_area_retangulo que receba a
# largura e a altura, calcule e retorne a área total. Solicite os valores
# ao usuário e exiba o resultado devolvido pela função.

def calcular_area_retangulo(largura, altura):
    return largura * altura


largura = float(input("Digite a largura do retângulo: ").replace(",", "."))
altura = float(input("Digite a altura do retângulo: ").replace(",", "."))
area = calcular_area_retangulo(largura, altura)

print(f"A área do retângulo é {area:.2f}.")
