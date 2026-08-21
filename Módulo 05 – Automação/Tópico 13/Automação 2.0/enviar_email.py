import smtplib
import os
from email.message import EmailMessage

destinatario = input("Digite o e-mail do destinatário: ")

mensagem = EmailMessage()

mensagem["From"] = "professor.rafael.selvagio@gmail.com"
mensagem["To"] = destinatario
mensagem["Subject"] = "Teste de automação"

mensagem.set_content("Olá! Este e-mail foi enviado automaticamente pelo Python.")

senha_app = os.getenv("EMAIL_SENHA")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
    servidor.login("professor.rafael.selvagio@gmail.com", senha_app)
    servidor.send_message(mensagem)