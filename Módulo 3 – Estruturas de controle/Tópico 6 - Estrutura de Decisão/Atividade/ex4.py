# ============================================================
# 4. Liberação de acesso a um sistema
# Desenvolva um programa em Python que solicite ao usuário um nome
# de usuário, uma senha e informe se o usuário está ativo. O acesso
# ao sistema deverá ser autorizado somente quando o nome de usuário
# for "admin", a senha for "1234" e o usuário estiver ativo. Se as
# três condições forem verdadeiras, exiba "Acesso autorizado".
# Caso contrário, exiba "Acesso negado".
# ============================================================

usuario = input("Digite o nome de usuário: ")
senha = input("Digite a senha: ")
ativo = input("O usuário está ativo? (sim/não): ").strip().lower()

if usuario == "admin" and senha == "1234" and ativo == "sim":
    print("Acesso autorizado")
else:
    print("Acesso negado")
