# ============================================================
# 2. Sistema de prioridade no atendimento
# Desenvolva um programa em Python que receba a idade de uma pessoa
# e informe se ela possui deficiência. O programa deverá verificar se
# a idade é maior ou igual a 60 anos ou se a pessoa possui deficiência.
# Caso pelo menos uma dessas condições seja verdadeira, exiba a
# mensagem Atendimento prioritário. Caso contrário, exiba
# Atendimento normal.
# ============================================================

idade = int(input("Digite a idade: "))
possui_deficiencia = input("Possui deficiência? (sim/não): ").strip().lower()

if idade >= 60 or possui_deficiencia  == "sim":
    print("Atendimento prioritário")
else:
    print("Atendimento normal")
