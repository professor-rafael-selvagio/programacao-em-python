# 3. Nota válida
# Solicite uma nota entre 0 e 10 até que o usuário informe um valor válido.
# Depois, exiba a nota recebida.

nota = float(input("Digite uma nota entre 0 e 10: ").replace(",", "."))

while nota < 0 or nota > 10:
    nota = float(input("Nota inválida. Digite uma nota entre 0 e 10: ").replace(",", "."))

print(f"Nota recebida: {nota:g}")
