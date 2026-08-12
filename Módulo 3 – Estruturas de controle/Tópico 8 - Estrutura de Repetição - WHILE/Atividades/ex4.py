# 4 - Exiba um menu de saldo, depósito e saída, repetindo até o usuário
# escolher sair. O saldo inicial é R$ 0,00.

saldo = 0.0
opcao = ""

while opcao != "0":
    print("\n1 - Ver saldo")
    print("2 - Depositar")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        print(f"Saldo atual: R$ {saldo:.2f}")
    elif opcao == "2":
        valor = float(input("Digite o valor do depósito: R$ ").replace(",", "."))
        if valor > 0:
            saldo += valor
            print("Depósito realizado com sucesso.")
        else:
            print("O valor do depósito deve ser positivo.")
    elif opcao == "0":
        print("Programa encerrado.")
    else:
        print("Opção inválida.")
