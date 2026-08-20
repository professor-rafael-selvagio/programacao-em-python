# 2. Número positivo
# Solicite números até que o usuário informe um número positivo.
# Depois, mostre a mensagem "Número válido!".

numero = float(input("Digite um número positivo: ").replace(",", "."))

while numero <= 0:
    numero = float(input("Número inválido. Digite um número positivo: ").replace(",", "."))

print("Número válido!")
