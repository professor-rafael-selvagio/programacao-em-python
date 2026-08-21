# --- ENTRADA ---
# Lê as duas notas informadas pelo usuário
nota1 = float(input("Digite a primeira nota: "))
nota2 = float(input("Digite a segunda nota: "))

# --- PROCESSAMENTO ---
# Calcula a média simples 
media = (nota1 + nota2) / 2

# --- SAÍDA ---
# Exibe o resultado da média
print("A média das notas é:", round(media, 2))