# Exercício 12: Crie funções para converter Celsius para Fahrenheit e
# Fahrenheit para Celsius. Faça um menu interativo e trate textos digitados
# no lugar da temperatura com try-except.

def celsius_para_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def fahrenheit_para_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


while True:
    print("\n1 - Celsius para Fahrenheit")
    print("2 - Fahrenheit para Celsius")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "0":
        print("Programa encerrado.")
        break

    if opcao not in ("1", "2"):
        print("Opção inválida.")
        continue

    try:
        temperatura = float(input("Digite a temperatura: ").replace(",", "."))
    except ValueError:
        print("Temperatura inválida. Digite um número.")
        continue

    if opcao == "1":
        resultado = celsius_para_fahrenheit(temperatura)
        print(f"Resultado: {resultado:.2f} °F")
    else:
        resultado = fahrenheit_para_celsius(temperatura)
        print(f"Resultado: {resultado:.2f} °C")
