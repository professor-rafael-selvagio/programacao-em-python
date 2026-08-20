from pathlib import Path
import shutil

# Pasta onde o desorganiza.py está localizado
pasta_programa = Path(__file__).resolve().parent

print("=== DESORGANIZADOR DE ARQUIVOS ===")

# Lista as pastas disponíveis
pastas_disponiveis = []

for item in pasta_programa.iterdir():

    if item.is_dir():
        pastas_disponiveis.append(item)

# Exibe as opções
print("\n0 - Desorganizar a pasta atual")

for indice, pasta in enumerate(pastas_disponiveis, start=1):
    print(f"{indice} - {pasta.name}")

# Solicita a escolha do usuário
opcao = input("\nEscolha uma opção: ")

if opcao == "0":

    # Desorganiza a pasta onde o programa está localizado
    pasta_atual = pasta_programa

else:

    try:
        indice = int(opcao) - 1
        pasta_atual = pastas_disponiveis[indice]

    except (ValueError, IndexError):
        print("Opção inválida.")
        exit()

print(f"\nPasta selecionada: {pasta_atual}")

# Pastas que serão desfeitas
pastas = [
    "Documentos",
    "Imagens",
    "Planilhas",
    "Programas",
    "Multimidia",
    "Compactados",
    "Logs"
]

# Percorre as pastas organizadas
for nome_pasta in pastas:

    pasta = pasta_atual / nome_pasta

    # Verifica se a pasta existe
    if pasta.exists() and pasta.is_dir():

        # Percorre todos os arquivos da pasta
        for arquivo in pasta.iterdir():

            if arquivo.is_file():

                # Move o arquivo para a pasta principal
                destino = pasta_atual / arquivo.name

                shutil.move(
                    str(arquivo),
                    str(destino)
                )

                print(
                    f"{arquivo.name} movido para a pasta principal."
                )

        # Exclui a pasta vazia
        pasta.rmdir()

        print(f"Pasta '{nome_pasta}' excluída.")

print("\nProcesso concluído!")