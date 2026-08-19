from pathlib import Path
import shutil

# Pasta onde este arquivo está localizado
pasta_atual = Path(__file__).resolve().parent

# Pastas que serão desfeitas
pastas = [
    "Documentos",
    "Imagens",
    "Planilhas",
    "Programas",
    "Multimidia",
    "Compactados",
]

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

                print(f"{arquivo.name} movido para a pasta principal.")

        # Exclui a pasta vazia
        pasta.rmdir()

        print(f"Pasta '{nome_pasta}' excluída.")

print("\nProcesso concluído!")
