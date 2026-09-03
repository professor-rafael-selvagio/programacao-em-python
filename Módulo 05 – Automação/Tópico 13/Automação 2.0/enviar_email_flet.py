"""Envia um e-mail com anexo usando uma interface gráfica feita com Flet.

Antes de executar, coloque a senha de app do Gmail em ``pass.txt`` na mesma
pasta deste arquivo. Nunca use a senha normal da conta do Gmail.
"""

import mimetypes
import os
import smtplib
import threading
from email.message import EmailMessage
from pathlib import Path
from typing import Any

# Algumas instalações do Python no macOS não configuram automaticamente o
# arquivo de certificados raiz. O certifi fornece esse arquivo com segurança.
try:
    import certifi

    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except ImportError:
    pass

import flet as ft


REMETENTE = "professor.rafael.selvagio@gmail.com"



def enviar_email(
    destinatario: str,
    assunto: str,
    texto: str,
    anexo: Path | None = None,
) -> None:
    """Monta e envia a mensagem pelo servidor SMTP do Gmail."""
    caminho_senha = Path(__file__).parent / "pass.txt"
    if not caminho_senha.is_file():
        raise FileNotFoundError(
            f"Arquivo de senha não encontrado: {caminho_senha.name}"
        )

    with open(caminho_senha, "r", encoding="utf-8") as arquivo:
        senha = arquivo.read().strip()
    if not senha:
        raise ValueError("O arquivo pass.txt está vazio.")

    mensagem = EmailMessage()
    mensagem["From"] = REMETENTE
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto
    mensagem.set_content(texto)

    if anexo is not None:
        tipo_mime, _ = mimetypes.guess_type(anexo.name)
        tipo_mime = tipo_mime or "application/octet-stream"
        tipo, subtipo = tipo_mime.split("/", 1)

        with anexo.open("rb") as arquivo:
            mensagem.add_attachment(
                arquivo.read(),
                maintype=tipo,
                subtype=subtipo,
                filename=anexo.name,
            )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(REMETENTE, senha)
        servidor.send_message(mensagem)


def main(page: Any) -> None:
    page.title = "Envio de e-mail automático"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 24
    page.window_width = 680
    page.window_height = 720
    page.scroll = ft.ScrollMode.AUTO

    destinatario = ft.TextField(
        label="E-mail do destinatário",
        hint_text="exemplo@dominio.com",
        keyboard_type=ft.KeyboardType.EMAIL,
        autofocus=True,
    )
    assunto = ft.TextField(label="Assunto", value="Teste de automação")
    texto = ft.TextField(
        label="Mensagem",
        value="Olá! Este e-mail foi enviado automaticamente pelo Python.",
        multiline=True,
        min_lines=5,
        max_lines=8,
    )
    anexo_selecionado: Path | None = None
    nome_anexo = ft.Text("Nenhum arquivo selecionado", color=ft.Colors.GREY_700)
    status = ft.Text()
    enviar = ft.ElevatedButton("Enviar e-mail", icon=ft.Icons.SEND)

    def aplicar_arquivo_escolhido(arquivo: Any) -> None:
        nonlocal anexo_selecionado
        caminho = getattr(arquivo, "path", None)
        if caminho:
            anexo_selecionado = Path(caminho)
            nome_anexo.value = f"Anexo: {anexo_selecionado.name}"
            nome_anexo.color = ft.Colors.GREEN_700
        page.update()

    # Na versão atual, pick_files() é uma coroutine e retorna os arquivos.
    async def escolher_anexo(_: Any) -> None:
        arquivos = await arquivo_picker.pick_files(
            dialog_title="Escolha o arquivo para anexar",
            allow_multiple=False,
        )
        if arquivos:
            aplicar_arquivo_escolhido(arquivos[0])

    # A anotação FilePickerResultEvent não existe em algumas versões do Flet.
    def arquivo_escolhido(event: Any) -> None:
        if event.files:
            aplicar_arquivo_escolhido(event.files[0])

    def mostrar_status(mensagem: str, cor: str) -> None:
        status.value = mensagem
        status.color = cor
        enviar.disabled = False
        page.update()

    def concluir_envio(
        destinatario_valor: str,
        assunto_valor: str,
        texto_valor: str,
        anexo_valor: Path | None,
    ) -> None:
        try:
            enviar_email(
                destinatario_valor,
                assunto_valor,
                texto_valor,
                anexo_valor,
            )
        except (OSError, smtplib.SMTPException, ValueError) as erro:
            mostrar_status(f"Não foi possível enviar: {erro}", ft.Colors.RED_700)
        else:
            mostrar_status(
                (
                    f"E-mail enviado com sucesso! Anexo: {anexo_valor.name}"
                    if anexo_valor
                    else "E-mail enviado com sucesso, sem anexo!"
                ),
                ft.Colors.GREEN_700,
            )

    def enviar_clicado(_: Any) -> None:
        if not destinatario.value or "@" not in destinatario.value:
            mostrar_status("Informe um e-mail de destinatário válido.", ft.Colors.RED_700)
            return
        if not assunto.value:
            mostrar_status("Informe o assunto da mensagem.", ft.Colors.RED_700)
            return
        if not texto.value:
            mostrar_status("Informe o texto da mensagem.", ft.Colors.RED_700)
            return
        enviar.disabled = True
        status.value = "Enviando e-mail..."
        status.color = ft.Colors.BLUE_700
        page.update()
        threading.Thread(
            target=concluir_envio,
            args=(destinatario.value, assunto.value, texto.value, anexo_selecionado),
            daemon=True,
        ).start()

    arquivo_picker = ft.FilePicker()
    if hasattr(arquivo_picker, "on_result"):
        arquivo_picker.on_result = arquivo_escolhido
    colecao_servicos = getattr(page, "services", None)
    if colecao_servicos is not None:
        colecao_servicos.append(arquivo_picker)
    else:
        page.overlay.append(arquivo_picker)
    enviar.on_click = enviar_clicado

    page.add(
        ft.Column(
            [
                ft.Text("Envio de e-mail automático", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(f"Remetente: {REMETENTE}", color=ft.Colors.GREY_700),
                destinatario,
                assunto,
                texto,
                ft.Row(
                    [
                        ft.OutlinedButton("Escolher anexo", icon=ft.Icons.ATTACH_FILE, on_click=escolher_anexo),
                        nome_anexo,
                    ],
                    wrap=True,
                ),
                enviar,
                status,
            ],
            spacing=16,
        )
    )


if __name__ == "__main__":
    ft.run(main)
