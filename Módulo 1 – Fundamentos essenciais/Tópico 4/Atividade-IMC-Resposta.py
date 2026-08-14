# --- ENTRADA ---
# Solicita o peso (kg) do usuário
peso = float(input("Digite o seu peso (kg): "))
# Solicita a altura (m) do usuário
altura = float(input("Digite a sua altura (metros): "))

# --- PROCESSAMENTO ---
# Calcula o IMC
imc = peso / (altura ** 2)

# --- SAÍDA ---
# Exibe o resultado arredondado para 2 casas decimais 
# usando a função round()
print("O seu IMC é:", round(imc, 2))