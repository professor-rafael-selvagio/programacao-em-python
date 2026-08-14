import tkinter as tk
from tkinter import ttk, messagebox

from autenticacao import (
    autenticar,
    carregar_usuarios,
    usuario_e_administrador
)


class SistemaLogin:

    def __init__(self, janela):

        self.janela = janela

        self.janela.title("Sistema de Login")

        self.janela.geometry("450x380")

        self.janela.resizable(
            False,
            False
        )

        self.configurar_estilo()

        self.criar_tela_login()

        # Tecla Enter executa a mesma função do botão
        self.janela.bind(
            "<Return>",
            lambda evento: self.realizar_login()
        )


    def configurar_estilo(self):

        estilo = ttk.Style()

        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure(
            "Titulo.TLabel",
            font=("Arial", 22, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            font=("Arial", 10)
        )

        estilo.configure(
            "Campo.TLabel",
            font=("Arial", 10, "bold")
        )

        estilo.configure(
            "Botao.TButton",
            font=("Arial", 11, "bold")
        )


    def criar_tela_login(self):

        self.frame = ttk.Frame(
            self.janela,
            padding=35
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        # Título
        ttk.Label(
            self.frame,
            text="Sistema de Login",
            style="Titulo.TLabel"
        ).pack(
            pady=(15, 5)
        )

        # Subtítulo
        ttk.Label(
            self.frame,
            text="Informe seus dados para acessar o sistema.",
            style="Subtitulo.TLabel"
        ).pack(
            pady=(0, 25)
        )

        # Login
        ttk.Label(
            self.frame,
            text="Login",
            style="Campo.TLabel"
        ).pack(
            anchor="w"
        )

        self.entry_login = ttk.Entry(
            self.frame,
            width=40
        )

        self.entry_login.pack(
            fill="x",
            pady=(5, 15)
        )

        # Senha
        ttk.Label(
            self.frame,
            text="Senha",
            style="Campo.TLabel"
        ).pack(
            anchor="w"
        )

        self.entry_senha = ttk.Entry(
            self.frame,
            width=40,
            show="*"
        )

        self.entry_senha.pack(
            fill="x",
            pady=(5, 20)
        )

        # Botão
        self.botao_entrar = ttk.Button(
            self.frame,
            text="Entrar",
            style="Botao.TButton",
            command=self.realizar_login
        )

        self.botao_entrar.pack(
            fill="x",
            ipady=5
        )

        self.entry_login.focus()


    def realizar_login(self):

        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        # ==========================================
        # 1. CAMPOS VAZIOS
        # ==========================================

        if not login or not senha:

            messagebox.showwarning(
                "Campos obrigatórios",
                "Todos os campos devem ser preenchidos.",
                parent=self.janela
            )

            return

        # ==========================================
        # AUTENTICAÇÃO
        # ==========================================

        try:

            resultado = autenticar(
                login,
                senha
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self.janela
            )

            return

        # ==========================================
        # 2. LOGIN OU SENHA INCORRETOS
        # ==========================================

        if not resultado["sucesso"]:

            if resultado["tipo"] == "credenciais":

                messagebox.showerror(
                    "Acesso negado",
                    resultado["mensagem"],
                    parent=self.janela
                )

            # ======================================
            # 3. USUÁRIO INATIVO
            # ======================================

            elif resultado["tipo"] == "inativo":

                messagebox.showwarning(
                    "Usuário inativo",
                    resultado["mensagem"],
                    parent=self.janela
                )

            return

        # ==========================================
        # 4. LOGIN REALIZADO
        # ==========================================

        usuario = resultado["usuario"]

        messagebox.showinfo(
            "Login realizado",
            resultado["mensagem"],
            parent=self.janela
        )

        # ==========================================
        # CONTROLE DE ACESSO ADMINISTRATIVO
        # ==========================================

        if usuario_e_administrador(usuario):

            self.abrir_area_administrativa()

        self.entry_senha.delete(
            0,
            tk.END
        )


    def abrir_area_administrativa(self):

        try:

            usuarios = carregar_usuarios()

        except Exception as erro:

            messagebox.showerror(
                "Erro na planilha",
                str(erro),
                parent=self.janela
            )

            return

        # Nova janela
        janela_admin = tk.Toplevel(
            self.janela
        )

        janela_admin.title(
            "Área Administrativa"
        )

        janela_admin.geometry(
            "800x450"
        )

        janela_admin.minsize(
            700,
            400
        )

        frame = ttk.Frame(
            janela_admin,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        # ==========================================
        # TÍTULO
        # ==========================================

        ttk.Label(
            frame,
            text="Área Administrativa",
            style="Titulo.TLabel"
        ).pack(
            anchor="w"
        )

        # ==========================================
        # CONTADOR
        # ==========================================

        ttk.Label(
            frame,
            text=f"Total de usuários cadastrados: {len(usuarios)}",
            style="Subtitulo.TLabel"
        ).pack(
            anchor="w",
            pady=(5, 15)
        )

        # ==========================================
        # ÁREA DA TABELA
        # ==========================================

        tabela_frame = ttk.Frame(frame)

        tabela_frame.pack(
            fill="both",
            expand=True
        )

        colunas = (
            "Nome",
            "Login",
            "Senha",
            "Status",
            "Nível"
        )

        tabela = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings"
        )

        # Cabeçalhos
        for coluna in colunas:

            tabela.heading(
                coluna,
                text=coluna
            )

        # Largura das colunas
        tabela.column(
            "Nome",
            width=200
        )

        tabela.column(
            "Login",
            width=120
        )

        tabela.column(
            "Senha",
            width=100
        )

        tabela.column(
            "Status",
            width=100
        )

        tabela.column(
            "Nível",
            width=150
        )

        # ==========================================
        # SCROLL VERTICAL
        # ==========================================

        scrollbar_vertical = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=tabela.yview
        )

        tabela.configure(
            yscrollcommand=scrollbar_vertical.set
        )

        # ==========================================
        # SCROLL HORIZONTAL
        # ==========================================

        scrollbar_horizontal = ttk.Scrollbar(
            tabela_frame,
            orient="horizontal",
            command=tabela.xview
        )

        tabela.configure(
            xscrollcommand=scrollbar_horizontal.set
        )

        tabela.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scrollbar_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        tabela_frame.rowconfigure(
            0,
            weight=1
        )

        tabela_frame.columnconfigure(
            0,
            weight=1
        )

        # ==========================================
        # INSERE OS USUÁRIOS
        # ==========================================

        for usuario in usuarios:

            tabela.insert(
                "",
                "end",
                values=(
                    usuario["Nome"],
                    usuario["Login"],
                    usuario["Senha"],
                    usuario["Status"],
                    usuario["Nível"]
                )
            )

        # ==========================================
        # BOTÃO FECHAR
        # ==========================================

        ttk.Button(
            frame,
            text="Fechar",
            command=janela_admin.destroy
        ).pack(
            anchor="e",
            pady=(15, 0)
        )


def iniciar_interface():

    janela = tk.Tk()

    SistemaLogin(janela)

    janela.mainloop()