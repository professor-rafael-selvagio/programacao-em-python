import imaplib
import email
import smtplib
from email.message import EmailMessage
from pathlib import Path


# ==========================================
# CONFIGURAÇÕES
# ==========================================
EMAIL = "professor.rafael.selvagio@gmail.com"

# Palavra que será procurada no assunto
ASSUNTO_FILTRO = "PythonA14T1"

# Resposta automática
RESPOSTA = """
Olá!

Se você recebeu este e-mail, significa que o exercício foi realizado com sucesso! 🎉

Esta mensagem foi enviada automaticamente pelo seu programa em Python.

Parabéns pela automação!

Atenciosamente,

Professor Rafael
"""


# ==========================================
# LER SENHA
# ==========================================
caminho_senha = Path(__file__).parent / "pass.txt"

with open(caminho_senha, "r") as arquivo:
    senha_app = arquivo.read().strip()

# ==========================================
# ACESSAR CAIXA DE ENTRADA
# ==========================================
with imaplib.IMAP4_SSL("imap.gmail.com", 993) as caixa:
    caixa.login(EMAIL, senha_app)
    caixa.select("INBOX")

    # Procura apenas mensagens não lidas
    status, mensagens = caixa.search(None, "UNSEEN")
    ids = mensagens[0].split()

    print(f"{len(ids)} e-mail(s) não lido(s) encontrado(s).")

    # ==========================================
    # ANALISAR CADA E-MAIL
    # ==========================================
    for id_email in ids:
        status, dados = caixa.fetch(id_email, "(RFC822)")
        mensagem_recebida = email.message_from_bytes(dados[0][1])
        remetente = mensagem_recebida["From"]
        assunto = mensagem_recebida["Subject"]

        print()
        print("Remetente:", remetente)
        print("Assunto:", assunto)

        # ==========================================
        # FILTRAR PELO ASSUNTO
        # ==========================================
        if assunto and ASSUNTO_FILTRO.lower() in assunto.lower():
            print("Assunto encontrado!")
            print("Enviando resposta automática...")

            # ==========================================
            # CRIAR RESPOSTA
            # ==========================================
            resposta = EmailMessage()
            resposta["From"] = EMAIL

            # Extrai o endereço do remetente
            endereco = email.utils.parseaddr(remetente)[1]
            resposta["To"] = endereco
            resposta["Subject"] = "Re: " + assunto
            resposta.set_content(RESPOSTA)

            # ==========================================
            # ENVIAR RESPOSTA
            # ==========================================
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
                servidor.login(EMAIL, senha_app)
                servidor.send_message(resposta)

            print("Resposta enviada com sucesso!")
        else:
            print("Assunto não corresponde ao filtro.")

    # ==========================================
    # ENCERRAR
    # ==========================================
    caixa.logout()

print()
print("Processamento concluído.")