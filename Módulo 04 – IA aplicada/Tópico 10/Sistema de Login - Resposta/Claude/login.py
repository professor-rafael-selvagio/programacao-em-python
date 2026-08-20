"""
interface.py
------------
Camada de interface gráfica (frontend) do sistema de login, construída
com Tkinter. Depende de dados.py para toda a lógica de autenticação e
leitura da planilha — nenhuma regra de negócio fica aqui.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import dados


class TelaLogin(tk.Tk):
    """Janela principal: formulário de login."""

    def __init__(self):
        super().__init__()

        self.title("Sistema de Login")
        self.geometry("360x220")
        self.resizable(False, False)

        # Usuários carregados da planilha ficam guardados aqui para
        # serem reutilizados na validação e, se for o caso, na tela
        # de administração — evita reabrir o arquivo a cada tentativa.
        self.usuarios = []

        self._montar_layout()
        self._carregar_dados_iniciais()

    # ------------------------------------------------------------------
    # Montagem visual da tela
    # ------------------------------------------------------------------
    def _montar_layout(self):
        """Cria e posiciona os widgets da tela de login."""
        container = ttk.Frame(self, padding=20)
        container.pack(expand=True, fill="both")

        titulo = ttk.Label(container, text="Login do Sistema", font=("Segoe UI", 14, "bold"))
        titulo.pack(pady=(0, 15))

        # --- Campo Login ---
        ttk.Label(container, text="Login:").pack(anchor="w")
        self.entrada_login = ttk.Entry(container)
        self.entrada_login.pack(fill="x", pady=(0, 10))

        # --- Campo Senha (oculta com show="*") ---
        ttk.Label(container, text="Senha:").pack(anchor="w")
        self.entrada_senha = ttk.Entry(container, show="*")
        self.entrada_senha.pack(fill="x", pady=(0, 15))

        # Botão "Entrar"
        botao_entrar = ttk.Button(container, text="Entrar", command=self._tentar_login)
        botao_entrar.pack(fill="x")

        # Permite logar pressionando Enter em qualquer um dos dois campos.
        self.bind("<Return>", lambda evento: self._tentar_login())

        # Foco inicial no campo de login, para agilizar a digitação.
        self.entrada_login.focus_set()

    # ------------------------------------------------------------------
    # Carregamento dos dados da planilha
    # ------------------------------------------------------------------
    def _carregar_dados_iniciais(self):
        """
        Carrega os usuários da planilha assim que a tela é aberta.
        Se houver erro (arquivo ausente/corrompido), avisa o usuário
        e mantém a tela aberta, mas sem permitir login funcional.
        """
        try:
            self.usuarios = dados.carregar_usuarios()
        except dados.ErroCarregarPlanilha as erro:
            messagebox.showerror("Erro ao carregar planilha", str(erro))
            self.usuarios = []

    # ------------------------------------------------------------------
    # Lógica de clique/Enter no botão de login
    # ------------------------------------------------------------------
    def _tentar_login(self):
        """Lê os campos, chama a validação em dados.py e trata o resultado."""

        # Se a planilha não pôde ser carregada, tenta recarregar antes
        # de bloquear o usuário (ela pode ter sido corrigida nesse meio-tempo).
        if not self.usuarios:
            self._carregar_dados_iniciais()
            if not self.usuarios:
                messagebox.showerror(
                    "Erro",
                    "Não há dados de usuários carregados. Corrija o arquivo e tente novamente."
                )
                return

        login = self.entrada_login.get()
        senha = self.entrada_senha.get()

        resultado, usuario = dados.autenticar(login, senha, self.usuarios)

        if resultado == "vazio":
            messagebox.showwarning("Campos obrigatórios", "Preencha login e senha.")

        elif resultado == "invalido":
            # Mensagem genérica: não indica se o erro foi no login ou na senha.
            messagebox.showerror("Erro de autenticação", "Login ou senha inválidos.")
            self.entrada_senha.delete(0, tk.END)

        elif resultado == "inativo":
            messagebox.showerror(
                "Usuário inativo",
                "Este usuário está inativo. Contate o administrador do sistema."
            )
            self.entrada_senha.delete(0, tk.END)

        elif resultado == "sucesso":
            messagebox.showinfo("Bem-vindo(a)", f"Bem-vindo(a), {usuario['Nome']}!")
            self._pos_login(usuario)

    # ------------------------------------------------------------------
    # O que acontece depois de um login bem-sucedido
    # ------------------------------------------------------------------
    def _pos_login(self, usuario):
        """
        Após autenticação bem-sucedida, limpa os campos e, se o usuário
        for Administrador, abre automaticamente a tela de administração.
        Usuários comuns não recebem nenhum acesso a essa tela.
        """
        self.entrada_login.delete(0, tk.END)
        self.entrada_senha.delete(0, tk.END)

        if dados.eh_administrador(usuario):
            TelaAdministracao(self, self.usuarios)
        # Usuários com Nível = "Usuário" simplesmente permanecem na tela
        # de login após a mensagem de boas-vindas; nenhuma outra tela é aberta.


class TelaAdministracao(tk.Toplevel):
    """
    Janela secundária (Toplevel), aberta apenas para usuários Administrador.
    Exibe todos os usuários cadastrados em formato de tabela (Treeview).
    """

    def __init__(self, janela_pai, usuarios):
        super().__init__(janela_pai)

        self.title("Administração de Usuários")
        self.geometry("560x320")
        self.resizable(False, False)

        # Mantém o foco nessa janela até que o administrador a feche,
        # reforçando que o restrito acesso é exclusivo dela.
        self.transient(janela_pai)
        self.grab_set()

        self._montar_layout(usuarios)

    def _montar_layout(self, usuarios):
        container = ttk.Frame(self, padding=15)
        container.pack(expand=True, fill="both")

        titulo = ttk.Label(
            container, text="Usuários Cadastrados", font=("Segoe UI", 13, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 10))

        # --- Tabela (Treeview) com os dados dos usuários ---
        colunas = ("nome", "login", "senha", "status")
        tabela = ttk.Treeview(container, columns=colunas, show="headings", height=8)

        tabela.heading("nome", text="Nome")
        tabela.heading("login", text="Login")
        tabela.heading("senha", text="Senha")
        tabela.heading("status", text="Status")

        tabela.column("nome", width=180)
        tabela.column("login", width=120)
        tabela.column("senha", width=100)
        tabela.column("status", width=80, anchor="center")

        for usuario in usuarios:
            tabela.insert("", tk.END, values=(
                usuario["Nome"], usuario["Login"], usuario["Senha"], usuario["Status"]
            ))

        tabela.pack(fill="both", expand=True, pady=(0, 10))

        # --- Rodapé: contador de usuários + botão fechar ---
        rodape = ttk.Frame(container)
        rodape.pack(fill="x")

        label_contador = ttk.Label(rodape, text=f"Total de usuários: {len(usuarios)}")
        label_contador.pack(side="left")

        botao_fechar = ttk.Button(rodape, text="Fechar", command=self.destroy)
        botao_fechar.pack(side="right")