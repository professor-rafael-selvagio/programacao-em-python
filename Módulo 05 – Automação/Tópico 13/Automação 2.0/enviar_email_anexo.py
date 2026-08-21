import smtplib
import mimetypes
import os
from pathlib import Path
from getpass import getpass
from email.message import EmailMessage


# E-mail que enviará a mensagem
remetente = "professor.rafael.selvagio@gmail.com"

# Solicita o destinatário
destinatario = input("Digite o e-mail do destinatário: ")

# Solicita a senha de app
caminho_senha = Path(__file__).parent / "pass.txt"
with open(caminho_senha, "r") as arquivo:
    senha = arquivo.read().strip()


# Pasta onde este arquivo Python está localizado
pasta_programa = Path(__file__).resolve().parent


# Lista os arquivos da pasta
arquivos = [
    arquivo
    for arquivo in pasta_programa.iterdir()
    if arquivo.is_file()
]


# Exibe os arquivos disponíveis
print("\nArquivos disponíveis:")

for indice, arquivo in enumerate(arquivos, start=1):
    print(f"{indice} - {arquivo.name}")


# Solicita a escolha do arquivo
opcao = int(input("\nEscolha o arquivo para anexar: "))

arquivo_anexo = arquivos[opcao - 1]


# Cria a mensagem
mensagem = EmailMessage()

mensagem["From"] = remetente
mensagem["To"] = destinatario
mensagem["Subject"] = "Teste de automação"

mensagem.set_content(
    "Olá! Este e-mail foi enviado automaticamente pelo Python."
)


# Identifica o tipo do arquivo
tipo_mime, _ = mimetypes.guess_type(arquivo_anexo)

if tipo_mime is None:
    tipo_mime = "application/octet-stream"

tipo, subtipo = tipo_mime.split("/", 1)


# Abre o arquivo e adiciona como anexo
with open(arquivo_anexo, "rb") as arquivo:
    mensagem.add_attachment(
        arquivo.read(),
        maintype=tipo,
        subtype=subtipo,
        filename=arquivo_anexo.name
    )


# Conecta ao Gmail e envia o e-mail
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:

    servidor.login(remetente, senha)

    servidor.send_message(mensagem)


print("\nE-mail enviado com sucesso!")
print(f"Anexo: {arquivo_anexo.name}")