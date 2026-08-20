# 6 - Solicite a idade de 5 pessoas e informe a média das idades.

soma_idades = 0

for pessoa in range(1, 6):
    idade = int(input(f"Digite a idade da pessoa {pessoa}: "))
    soma_idades += idade

media = soma_idades / 5
print(f"A média das idades é {media:.2f} anos.")
