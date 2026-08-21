from pathlib import Path
import shutil
import time

# Pasta onde o arquivo organiza.py está localizado
pasta_programa = Path(__file__).resolve().parent

print("=== ORGANIZADOR DE ARQUIVOS ===")

# Lista onde serão armazenadas as pastas disponíveis
pastas_disponiveis = []

# Procura todas as pastas no diretório do programa
for item in pasta_programa.iterdir():

    if item.is_dir():
        pastas_disponiveis.append(item)

# Exibe as opções
print("\n0 - Organizar a pasta atual")

for indice, pasta in enumerate(pastas_disponiveis, start=1):
    print(f"{indice} - {pasta.name}")

# Solicita a escolha do usuário
opcao = input("\nEscolha uma opção: ")

if opcao == "0":

    # Organiza a pasta onde o programa está localizado
    pasta_atual = pasta_programa

else:

    try:
        indice = int(opcao) - 1
        pasta_atual = pastas_disponiveis[indice]

    except (ValueError, IndexError):
        print("Opção inválida.")
        exit()

print(f"\nPasta selecionada: {pasta_atual}")

# Arquivos que não serão organizados
excecoes = [
    "organiza.py",
    "desorganiza.py",
    "Atividade.txt"
]

# Extensões de cada categoria
tipos = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documentos": [".txt", ".pdf", ".doc", ".docx"],
    "Planilhas": [".xls", ".xlsx", ".csv"],
    "Programas": [".py", ".json", ".html", ".xml"],
    "Multimidia": [".mp3", ".mp4"],
    "Compactados": [".zip"],
    "Logs": [".log"]
}

# Cria o contador de arquivos organizados
contador_arquivos = 0

# Registra o tempo de início da organização
inicio = time.time()

# Percorre todos os arquivos da pasta selecionada
for arquivo in pasta_atual.iterdir():

    # Ignora pastas
    if arquivo.is_file():

        # Conta o número de arquivos organizados
        contador_arquivos += 1

        # Ignora arquivos da lista de exceções
        if arquivo.name in excecoes:
            print(f"{arquivo.name} -> Ignorado")
            continue

        # Obtém a extensão do arquivo
        extensao = arquivo.suffix.lower()

        # Verifica a categoria do arquivo
        for categoria, extensoes in tipos.items():

            if extensao in extensoes:

                # Cria a pasta de destino
                pasta_destino = pasta_atual / categoria
                pasta_destino.mkdir(exist_ok=True)

                # Move o arquivo
                shutil.move(
                    str(arquivo),
                    str(pasta_destino / arquivo.name)
                )

                print(f"{arquivo.name} -> {categoria}")
                break

# Registra o tempo de fim da organização
fim = time.time()

# Calcula o tempo de execução
tempo = fim - inicio

print(f"\nA organização de {contador_arquivos} arquivos foi concluída em {tempo:.2f} segundos.")