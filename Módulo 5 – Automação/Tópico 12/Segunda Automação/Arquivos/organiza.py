from pathlib import Path
import shutil

# Pasta onde o programa está sendo executado
pasta_atual = Path(__file__).resolve().parent

# Extensões de cada categoria
tipos = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documentos": [".txt", ".pdf", ".doc", ".docx"],
    "Planilhas": [".xls", ".xlsx", ".csv"],
    "Programas": [".py", ".json", ".html", ".xml"],
    "Multimidia": [".mp3", ".mp4"],
    "Compactados": [".zip"]
}

# Percorre todos os arquivos da pasta atual
for arquivo in pasta_atual.iterdir():

    # Ignora pastas
    if arquivo.is_file():

        # Obtém a extensão do arquivo
        extensao = arquivo.suffix.lower()

        # Verifica a qual categoria o arquivo pertence
        for categoria, extensoes in tipos.items():

            if extensao in extensoes:

                # Cria a subpasta, caso ela não exista
                pasta_destino = pasta_atual / categoria
                pasta_destino.mkdir(exist_ok=True)

                # Move o arquivo para a subpasta
                shutil.move(
                    str(arquivo),
                    str(pasta_destino / arquivo.name)
                )

                print(f"{arquivo.name} -> {categoria}")
                break
