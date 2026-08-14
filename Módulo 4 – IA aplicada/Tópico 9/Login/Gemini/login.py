import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from pathlib import Path

# ==========================================
# CONFIGURAÇÕES E CONSTANTES
# ==========================================
ARQUIVO_EXCEL = Path(__file__).resolve().parent / "usuarios.xlsx"
COLUNAS_ESPERADAS = ["Nome", "Login", "Senha", "Status", "Nível"]


# ==========================================
# CAMADA DE DADOS E REGRA DE NEGÓCIO
# ==========================================
class GerenciadorAutenticacao:
    """Classe ajustada para ler perfeitamente a sua planilha existente."""

    def __init__(self, caminho_arquivo=ARQUIVO_EXCEL):
        self.caminho_arquivo = caminho_arquivo

    def carregar_usuarios(self):
        """Lê a planilha Excel sem recriá-la e trata os dados."""
        try:
            # Lê todas as colunas como string para evitar perdas de formatação
            df = pd.read_excel(self.caminho_arquivo, dtype=str)
            df = df.fillna("")

            # Garante que as colunas obrigatórias existem
            for coluna in COLUNAS_ESPERADAS:
                if coluna not in df.columns:
                    raise ValueError(f"Coluna obrigatória ausente na planilha: '{coluna}'")

            # Remove espaços acidentais de todas as células
            for col in COLUNAS_ESPERADAS:
                df[col] = df[col].astype(str).str.strip()

            return df
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar a planilha Excel: {e}")

    def autenticar(self, login, senha):
        """Realiza a autenticação com validação estrita."""
        login_limpo = str(login).strip().lower()
        senha_limpa = str(senha).strip()

        # 1. Validação de campos vazios
        if not login_limpo or not senha_limpa:
            return False, "Por favor, preencha todos os campos.", None

        # Carrega os dados da planilha existente
        df = self.carregar_usuarios()

        # Busca pelo login (case-insensitive)
        usuario_match = df[df["Login"].str.lower() == login_limpo]

        # 2. Login ou Senha incorretos
        if usuario_match.empty:
            return False, "Login ou senha incorretos.", None

        usuario = usuario_match.iloc[0]

        # Compara a senha exata
        if usuario["Senha"] != senha_limpa:
            return False, "Login ou senha incorretos.", None

        # 3. Validação de usuário inativo (Aceita "Ativo" e rejeita "Desativado" / "Inativo")
        status_normalizado = usuario["Status"].capitalize()
        if status_normalizado != "Ativo":
            return False, "Usuário inativo. Contate o administrador.", None

        # 4. Sucesso na autenticação
        dados_usuario = {
            "Nome": usuario["Nome"],
            "Login": usuario["Login"],
            "Status": usuario["Status"],
            "Nível": usuario["Nível"],
        }
        return True, f"Bem-vindo(a), {usuario['Nome']}!", dados_usuario


# ==========================================
# INTERFACE GRÁFICA (TKINTER)
# ==========================================
class JanelaPainelAdmin(tk.Toplevel):
    """Tela secundária exibida para Administradores."""

    def __init__(self, parent, gerencia_auth):
        super().__init__(parent)
        self.gerencia_auth = gerencia_auth

        self.title("Painel Administrativo - Gestão de Usuários")
        self.geometry("650x400")
        self.resizable(False, False)

        # Torna a janela modal
        self.transient(parent)
        self.grab_set()

        self._criar_interface()
        self._carregar_dados_tabela()

    def _criar_interface(self):
        lbl_titulo = tk.Label(
            self,
            text="Lista de Usuários Cadastrados",
            font=("Helvetica", 14, "bold"),
            pady=10,
        )
        lbl_titulo.pack(side=tk.TOP, fill=tk.X)

        frame_tabela = ttk.Frame(self, padding=10)
        frame_tabela.pack(expand=True, fill=tk.BOTH)

        colunas = ("Nome", "Login", "Senha", "Status", "Nível")
        self.tree = ttk.Treeview(
            frame_tabela, columns=colunas, show="headings", height=10
        )

        larguras = {
            "Nome": 150,
            "Login": 100,
            "Senha": 100,
            "Status": 90,
            "Nível": 120,
        }
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(
                col, width=larguras[col], anchor=tk.CENTER if col != "Nome" else tk.W
            )

        scrollbar = ttk.Scrollbar(
            frame_tabela, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame_rodape = ttk.Frame(self, padding=10)
        frame_rodape.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_contador = ttk.Label(
            frame_rodape, text="Total de usuários: 0", font=("Helvetica", 10)
        )
        self.lbl_contador.pack(side=tk.LEFT)

        btn_fechar = ttk.Button(
            frame_rodape, text="Fechar", command=self.destroy
        )
        btn_fechar.pack(side=tk.RIGHT)

    def _carregar_dados_tabela(self):
        try:
            df = self.gerencia_auth.carregar_usuarios()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for _, row in df.iterrows():
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        row["Nome"],
                        row["Login"],
                        row["Senha"],
                        row["Status"],
                        row["Nível"],
                    ),
                )

            self.lbl_contador.config(text=f"Total de usuários: {len(df)}")

        except Exception as e:
            messagebox.showerror("Erro de Leitura", f"Erro na tabela: {e}")


class AppLogin(tk.Tk):
    """Janela Principal de Login."""

    def __init__(self):
        super().__init__()
        self.title("Acesso ao Sistema")
        self.geometry("360x260")
        self.resizable(False, False)

        try:
            self.gerencia_auth = GerenciadorAutenticacao()
        except Exception as e:
            messagebox.showerror("Erro Crítico", str(e))
            self.destroy()
            return

        self._centralizar_janela()
        self._criar_interface()

    def _centralizar_janela(self):
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        pos_x = (self.winfo_screenwidth() // 2) - (largura // 2)
        pos_y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def _criar_interface(self):
        container = ttk.Frame(self, padding=20)
        container.pack(expand=True, fill=tk.BOTH)

        lbl_titulo = ttk.Label(
            container, text="Login do Sistema", font=("Helvetica", 14, "bold")
        )
        lbl_titulo.pack(pady=(0, 15))

        ttk.Label(container, text="Usuário:").pack(anchor=tk.W)
        self.ent_login = ttk.Entry(container, width=35)
        self.ent_login.pack(pady=(2, 10))
        self.ent_login.focus()

        ttk.Label(container, text="Senha:").pack(anchor=tk.W)
        self.ent_senha = ttk.Entry(container, show="*", width=35)
        self.ent_senha.pack(pady=(2, 15))

        self.btn_entrar = ttk.Button(
            container, text="Entrar", command=self._processar_login
        )
        self.btn_entrar.pack(fill=tk.X)

        self.bind("<Return>", lambda event: self._processar_login())

    def _processar_login(self):
        login = self.ent_login.get()
        senha = self.ent_senha.get()

        try:
            sucesso, mensagem, dados_usuario = self.gerencia_auth.autenticar(
                login, senha
            )

            if not sucesso:
                messagebox.showwarning("Aviso", mensagem)
                return

            messagebox.showinfo("Sucesso", mensagem)
            self.ent_senha.delete(0, tk.END)

            if str(dados_usuario["Nível"]).strip().capitalize() == "Administrador":
                JanelaPainelAdmin(self, self.gerencia_auth)

        except Exception as e:
            messagebox.showerror(
                "Erro no Sistema", f"Ocorreu um erro ao processar:\n{e}"
            )


if __name__ == "__main__":
    app = AppLogin()
    app.mainloop()