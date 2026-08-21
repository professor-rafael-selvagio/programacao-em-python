# Exercício 5: Solicite dois números inteiros e realize a divisão do primeiro
# pelo segundo. Utilize blocos try-except para tratar separadamente a inserção
# de texto e a tentativa de dividir por zero.

try:
    primeiro_numero = int(input("Digite o primeiro número inteiro: "))
    segundo_numero = int(input("Digite o segundo número inteiro: "))
    resultado = primeiro_numero / segundo_numero
except ValueError:
    print("Entrada inválida. Digite apenas números inteiros.")
except ZeroDivisionError:
    print("Não é possível dividir um número por zero.")
else:
    print(f"Resultado da divisão: {resultado}")
