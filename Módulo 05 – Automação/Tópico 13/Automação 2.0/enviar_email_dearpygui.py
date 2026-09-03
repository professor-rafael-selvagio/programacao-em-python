import smtplib
import mimetypes
import subprocess
from pathlib import Path
from email.message import EmailMessage

import dearpygui.dearpygui as dpg


# ============================================================
# CONFIGURAÇÕES
# ============================================================

REMETENTE = "professor.rafael.selvagio@gmail.com"
CAMINHO_SENHA = Path(__file__).parent / "pass.txt"

# --------------------------------------------------------------
# Guarda o caminho do anexo numa variável Python normal.
# Isso resolve o problema de "seleciona mas não anexa": o campo
# oculto do DPG às vezes atrasa 1 clique para atualizar o valor,
# enquanto uma variável Python é sempre confiável e imediata.
# --------------------------------------------------------------
ARQUIVO_SELECIONADO = None


# ============================================================
# FUNÇÃO PARA MOSTRAR STATUS
# ============================================================

def mostrar_status(texto):
    dpg.set_value("status", texto)


# ============================================================
# ENVIO DO E-MAIL
# ============================================================

def enviar_email():

    global ARQUIVO_SELECIONADO

    destinatario = dpg.get_value("destinatario").strip()
    assunto = dpg.get_value("assunto").strip()
    mensagem_texto = dpg.get_value("mensagem")

    # --------------------------------------------------------
    # VALIDAÇÕES
    # --------------------------------------------------------

    if not destinatario:
        mostrar_status("Digite o e-mail do destinatário.")
        return

    if not assunto:
        mostrar_status("Digite o assunto.")
        return

    if not mensagem_texto.strip():
        mostrar_status("Digite a mensagem.")
        return

    # --------------------------------------------------------
    # VERIFICA O ANEXO (lido da variável global, não do campo oculto)
    # --------------------------------------------------------

    arquivo_anexo = None

    if ARQUIVO_SELECIONADO:

        arquivo_anexo = Path(ARQUIVO_SELECIONADO)

        try:
            arquivo_anexo = arquivo_anexo.resolve()
        except Exception:
            pass

        print("=" * 60)
        print("CAMINHO DO ANEXO:", arquivo_anexo)
        print("EXISTE:", arquivo_anexo.exists())
        print("É ARQUIVO:", arquivo_anexo.is_file())
        print("=" * 60)

        if not arquivo_anexo.exists():
            mostrar_status(f"O arquivo não existe:\n{arquivo_anexo}")
            return

        if not arquivo_anexo.is_file():
            mostrar_status(f"O item selecionado não é um arquivo:\n{arquivo_anexo}")
            return

    # --------------------------------------------------------
    # LÊ A SENHA
    # --------------------------------------------------------

    if not CAMINHO_SENHA.exists():
        mostrar_status("Arquivo pass.txt não encontrado.")
        return

    try:
        with open(CAMINHO_SENHA, "r", encoding="utf-8") as arquivo:
            senha = arquivo.read().strip()
    except Exception as erro:
        mostrar_status(f"Erro ao ler pass.txt:\n{erro}")
        return

    if not senha:
        mostrar_status("A senha do e-mail está vazia.")
        return

    # --------------------------------------------------------
    # CRIA A MENSAGEM
    # --------------------------------------------------------

    try:
        mensagem = EmailMessage()
        mensagem["From"] = REMETENTE
        mensagem["To"] = destinatario
        mensagem["Subject"] = assunto
        mensagem.set_content(mensagem_texto)

        # ----------------------------------------------------
        # ADICIONA O ANEXO
        # ----------------------------------------------------

        if arquivo_anexo:

            mostrar_status(f"Preparando anexo:\n{arquivo_anexo.name}")

            tipo_mime, _ = mimetypes.guess_type(str(arquivo_anexo))

            if tipo_mime is None:
                tipo_mime = "application/octet-stream"

            tipo, subtipo = tipo_mime.split("/", 1)

            with open(arquivo_anexo, "rb") as arquivo:
                dados = arquivo.read()

            print("Arquivo anexado:")
            print("Nome:", arquivo_anexo.name)
            print("Tamanho:", len(dados), "bytes")
            print("MIME:", tipo_mime)

            mensagem.add_attachment(
                dados,
                maintype=tipo,
                subtype=subtipo,
                filename=arquivo_anexo.name
            )

        # ----------------------------------------------------
        # CONEXÃO COM GMAIL
        # ----------------------------------------------------

        mostrar_status("Conectando ao Gmail...")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(REMETENTE, senha)
            print("Login realizado com sucesso.")
            servidor.send_message(mensagem)

        # ----------------------------------------------------
        # SUCESSO
        # ----------------------------------------------------

        if arquivo_anexo:
            mostrar_status(
                "E-mail enviado com sucesso! 🎉\n"
                f"Anexo: {arquivo_anexo.name}"
            )
        else:
            mostrar_status("E-mail enviado com sucesso! 🎉")

    except smtplib.SMTPAuthenticationError:
        mostrar_status(
            "Erro de autenticação no Gmail.\n"
            "Verifique a senha de aplicativo no pass.txt."
        )

    except smtplib.SMTPException as erro:
        mostrar_status(f"Erro no servidor SMTP:\n{erro}")

    except PermissionError:
        mostrar_status("Sem permissão para acessar o arquivo.")

    except FileNotFoundError:
        mostrar_status("O arquivo selecionado não foi encontrado.")

    except Exception as erro:
        mostrar_status(f"Erro ao enviar o e-mail:\n{erro}")


# ============================================================
# SELEÇÃO DO ARQUIVO
# ============================================================

def escolher_arquivo_macos():
    """
    Abre o seletor de arquivos NATIVO do macOS via AppleScript.
    Roda como processo separado, então não conflita com o loop
    de janelas do DearPyGui (o que acontece quando se tenta usar
    Tkinter no mesmo processo no macOS).
    Retorna o caminho absoluto (str) ou None se o usuário cancelar.
    """

    script = 'POSIX path of (choose file with prompt "Selecione o arquivo para anexar")'

    try:
        resultado = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=300
        )
    except Exception as erro:
        print("Erro ao chamar osascript:", erro)
        return None

    if resultado.returncode != 0:
        # Usuário cancelou o diálogo (ou outro erro do AppleScript)
        print("Seleção cancelada ou erro:", resultado.stderr.strip())
        return None

    caminho = resultado.stdout.strip()

    return caminho if caminho else None


def selecionar_arquivo():

    global ARQUIVO_SELECIONADO

    caminho = escolher_arquivo_macos()

    print("\n" + "=" * 60)
    print("CAMINHO RETORNADO PELO OSASCRIPT:", caminho)
    print("=" * 60)

    if not caminho:
        mostrar_status("Nenhum arquivo foi selecionado.")
        return

    arquivo = Path(caminho)

    try:
        arquivo = arquivo.resolve()
    except Exception:
        pass

    if arquivo.is_dir():
        mostrar_status("Por favor, selecione um arquivo específico, não uma pasta.")
        return

    if not arquivo.exists():
        mostrar_status(f"Arquivo não encontrado no sistema:\n{arquivo}")
        return

    if not arquivo.is_file():
        mostrar_status("O item selecionado não é um arquivo válido.")
        return

    # Salva na variável global (fonte confiável) e também no campo oculto
    ARQUIVO_SELECIONADO = str(arquivo)
    dpg.set_value("arquivo", str(arquivo))
    dpg.set_value("nome_arquivo", arquivo.name)

    tamanho = arquivo.stat().st_size

    mostrar_status(
        f"Arquivo anexado com sucesso:\n"
        f"{arquivo.name}\n"
        f"Tamanho: {tamanho:,} bytes"
    )

    print("Arquivo salvo para envio:", arquivo)


# ============================================================
# LIMPAR ANEXO
# ============================================================

def limpar_anexo():

    global ARQUIVO_SELECIONADO

    ARQUIVO_SELECIONADO = None

    dpg.set_value("arquivo", "")
    dpg.set_value("nome_arquivo", "")

    mostrar_status("Anexo removido.")


# ============================================================
# CRIAÇÃO DO CONTEXTO
# ============================================================

dpg.create_context()


# ============================================================
# JANELA PRINCIPAL
# ============================================================

with dpg.window(label="Automação de E-mail", width=550, height=500):

    dpg.add_text("📧 Envio de E-mail com Python")
    dpg.add_separator()

    dpg.add_text("Destinatário:")
    dpg.add_input_text(tag="destinatario", hint="Digite o e-mail", width=-1)

    dpg.add_text("Assunto:")
    dpg.add_input_text(tag="assunto", hint="Digite o assunto", width=-1)

    dpg.add_text("Mensagem:")
    dpg.add_input_text(
        tag="mensagem",
        multiline=True,
        height=120,
        width=-1,
        hint="Digite sua mensagem..."
    )

    dpg.add_text("Anexo:")

    with dpg.group(horizontal=True):

        dpg.add_input_text(
            tag="nome_arquivo",
            readonly=True,
            width=330,
            hint="Nenhum arquivo selecionado"
        )

        dpg.add_button(
            label="Selecionar",
            callback=lambda: selecionar_arquivo()
        )

        dpg.add_button(label="X", callback=limpar_anexo, width=30)

    dpg.add_input_text(tag="arquivo", show=False)

    dpg.add_spacer(height=10)

    dpg.add_button(
        label="📨 ENVIAR E-MAIL",
        callback=enviar_email,
        width=-1,
        height=40
    )

    dpg.add_spacer(height=10)

    dpg.add_text("", tag="status", wrap=500)


# ============================================================
# VIEWPORT
# ============================================================

dpg.create_viewport(title="Automação de E-mail", width=570, height=550)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()