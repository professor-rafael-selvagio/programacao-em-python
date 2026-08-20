# ============================================================
# 3. Validação de acesso a um benefício
# Desenvolva um programa em Python que receba a idade de uma pessoa
# e sua renda mensal. O programa deverá verificar se a pessoa possui
# 18 anos ou mais e se sua renda mensal é menor ou igual a R$ 2.500,00.
# Caso as duas condições sejam verdadeiras, exiba a mensagem
# Pode solicitar o benefício. Caso contrário, exiba
# Não atende aos critérios.
# ============================================================

idade = int(input("Digite a idade: "))
renda = float(input("Digite a renda mensal: R$ ").replace(",", "."))

if idade >= 18 and renda <= 2500:
    print("Pode solicitar o benefício")
else:
    print("Não atende aos critérios")
