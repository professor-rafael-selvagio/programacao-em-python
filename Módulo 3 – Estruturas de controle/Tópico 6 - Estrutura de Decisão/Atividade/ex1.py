# ============================================================
# 1. Controle de acesso
# Desenvolva um programa em Python que solicite o nome e a idade
# de uma pessoa. Se a idade for maior ou igual a 18 anos, o acesso
# deverá ser liberado sem a necessidade de informar um responsável.
# Caso a idade seja menor de 18 anos, o programa deverá solicitar
# também o nome do responsável. Ao final, exiba uma mensagem contendo
# o nome da pessoa, sua idade, informando se possui responsável e,
# quando houver, o nome do responsável.
# ============================================================

nome = input("Digite o nome da pessoa: ")
idade = int(input("Digite a idade: "))

if idade >= 18:
    possui_responsavel = False
    responsavel = ""
else:
    possui_responsavel = True
    responsavel = input("Digite o nome do responsável: ")

print(f"Nome: {nome}")
print(f"Idade: {idade} anos")

if possui_responsavel:
    print(f"Possui responsável: Sim")
    print(f"Responsável: {responsavel}")
else:
    print(f"Possui responsável: Não")
