# 6 - Solicite a idade de 5 pessoas e informe a média das idades.

# Crie uma lista para armazenar as idades
lista_idades = []

# Crie a estrutura de repetição para solicitar a idade de 5 pessoas
for pessoa in range(1, 6):

    # Solicita a idade da pessoa e adiciona à lista
    idade = int(input(f"Digite a idade da pessoa {pessoa}: "))

    # Adiciona a idade à lista de idades
    lista_idades.append(idade)

# Calcula a média das idades usando a função sum() e len()
media = sum(lista_idades) / len(lista_idades)

# Exibe a médias das idades com duas casas decimais
print(f"A média das idades é {media:.2f} anos.")
