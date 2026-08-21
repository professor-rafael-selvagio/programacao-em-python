import smtplib
from email.message import EmailMessage
from pathlib import Path

destinatario = input("Digite o e-mail do destinatário: ")

mensagem = EmailMessage()

mensagem["From"] = "professor.rafael.selvagio@gmail.com"
mensagem["To"] = destinatario
mensagem["Subject"] = "Teste de automação"

mensagem.set_content("Olá! Este e-mail foi enviado automaticamente pelo Python.")

caminho_senha = Path(__file__).parent / "pass.txt"
with open(caminho_senha, "r") as arquivo:
    senha_app = arquivo.read().strip()

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
    servidor.login("professor.rafael.selvagio@gmail.com", senha_app)
    servidor.send_message(mensagem)