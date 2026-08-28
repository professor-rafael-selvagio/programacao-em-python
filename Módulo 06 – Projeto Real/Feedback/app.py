"""Aplicação local de Feedback de Turmas.

Execute com: python app.py
Os alunos acessam o endereço exibido pelo professor na mesma rede local.
"""

import csv
import io
import os
import secrets
import sqlite3
import uuid
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, session, url_for


PASTA_PROJETO = Path(__file__).resolve().parent
ARQUIVO_BANCO = PASTA_PROJETO / "banco.db"
ARQUIVO_PERGUNTAS = PASTA_PROJETO / "perguntas.csv"
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FEEDBACK_SECRET_KEY", "chave-didatica-troque-em-producao")
PROFESSOR_LOGIN = os.environ.get("PROFESSOR_LOGIN", "professor.rafael")
PROFESSOR_SENHA = os.environ.get("PROFESSOR_SENHA", "olimpico")


def conectar():
    banco = sqlite3.connect(ARQUIVO_BANCO)
    banco.row_factory = sqlite3.Row
    banco.execute("PRAGMA foreign_keys = ON")
    banco.execute("PRAGMA busy_timeout = 5000")
    return banco


def inicializar_banco():
    with conectar() as banco:
        banco.executescript("""
            CREATE TABLE IF NOT EXISTS sessoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                turma TEXT NOT NULL,
                token_controle TEXT NOT NULL UNIQUE,
                pergunta_atual INTEGER NOT NULL DEFAULT 0,
                encerrada INTEGER NOT NULL DEFAULT 0,
                protegida INTEGER NOT NULL DEFAULT 0,
                criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS perguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sessao_id INTEGER NOT NULL,
                ordem INTEGER NOT NULL,
                tipo TEXT NOT NULL CHECK (tipo IN ('nota', 'aberta')),
                texto TEXT NOT NULL,
                escala TEXT NOT NULL DEFAULT '',
                FOREIGN KEY (sessao_id) REFERENCES sessoes(id) ON DELETE CASCADE,
                UNIQUE (sessao_id, ordem)
            );
            CREATE TABLE IF NOT EXISTS respostas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sessao_id INTEGER NOT NULL,
                pergunta_id INTEGER NOT NULL,
                aluno_id TEXT NOT NULL,
                valor TEXT NOT NULL,
                respondida_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sessao_id) REFERENCES sessoes(id) ON DELETE CASCADE,
                FOREIGN KEY (pergunta_id) REFERENCES perguntas(id) ON DELETE CASCADE,
                UNIQUE (sessao_id, pergunta_id, aluno_id)
            );
            CREATE INDEX IF NOT EXISTS indice_respostas_pergunta
                ON respostas (sessao_id, pergunta_id);
        """)
        colunas = {linha[1] for linha in banco.execute("PRAGMA table_info(perguntas)")}
        if "escala" not in colunas:
            banco.execute("ALTER TABLE perguntas ADD COLUMN escala TEXT NOT NULL DEFAULT ''")
        colunas_sessoes = {linha[1] for linha in banco.execute("PRAGMA table_info(sessoes)")}
        if "protegida" not in colunas_sessoes:
            banco.execute("ALTER TABLE sessoes ADD COLUMN protegida INTEGER NOT NULL DEFAULT 0")


def carregar_csv(arquivo):
    conteudo = arquivo.read().decode("utf-8-sig") if arquivo else ARQUIVO_PERGUNTAS.read_text(encoding="utf-8-sig")
    leitor = csv.DictReader(io.StringIO(conteudo))
    obrigatorias = {"tipo", "pergunta"}
    if not leitor.fieldnames or not obrigatorias.issubset({campo.strip().lower() for campo in leitor.fieldnames}):
        raise ValueError("O CSV precisa ter as colunas 'tipo' e 'pergunta'.")
    perguntas = []
    for numero, linha in enumerate(leitor, 1):
        normalizada = {str(chave).strip().lower(): (valor or "").strip() for chave, valor in linha.items()}
        tipo, texto = normalizada.get("tipo", "").casefold(), normalizada.get("pergunta", "")
        if tipo not in {"nota", "aberta"}:
            raise ValueError(f"Linha {numero}: o tipo deve ser 'nota' ou 'aberta'.")
        if not texto:
            raise ValueError(f"Linha {numero}: a pergunta não pode ficar vazia.")
        perguntas.append((tipo, texto, normalizada.get("escala", "")))
    if not perguntas:
        raise ValueError("O CSV não contém perguntas.")
    return perguntas


def buscar_sessao(codigo):
    with conectar() as banco:
        return banco.execute("SELECT * FROM sessoes WHERE codigo = ?", (codigo,)).fetchone()


def sessao_autorizada(codigo, token):
    with conectar() as banco:
        return banco.execute(
            "SELECT * FROM sessoes WHERE codigo = ? AND token_controle = ?", (codigo, token)
        ).fetchone()


def id_aluno():
    if "aluno_id" not in session:
        session["aluno_id"] = uuid.uuid4().hex
    return session["aluno_id"]


def professor_logado():
    return session.get("professor_autenticado") is True


def exigir_professor(funcao):
    @wraps(funcao)
    def decorada(*args, **kwargs):
        if not professor_logado():
            return redirect(url_for("login_professor", proxima=request.path))
        return funcao(*args, **kwargs)
    return decorada


def pergunta_atual(codigo):
    sessao = buscar_sessao(codigo)
    if not sessao or sessao["encerrada"]:
        return sessao, None
    with conectar() as banco:
        pergunta = banco.execute(
            "SELECT * FROM perguntas WHERE sessao_id = ? AND ordem = ?",
            (sessao["id"], sessao["pergunta_atual"]),
        ).fetchone()
    return sessao, pergunta


def extrair_notas_validas(valores):
    """Converte somente respostas inteiras entre 0 e 10 para os relatórios."""
    notas = []
    for valor in valores:
        try:
            numero = int(str(valor).strip())
        except (TypeError, ValueError):
            continue
        if 0 <= numero <= 10 and str(numero) == str(valor).strip():
            notas.append(numero)
    return notas


@app.route("/login-professor", methods=["GET", "POST"])
def login_professor():
    proxima = request.args.get("proxima") or request.form.get("proxima") or url_for("criar_feedback")
    if request.method == "POST":
        login = request.form.get("login", "").strip()
        senha = request.form.get("senha", "")
        if login == PROFESSOR_LOGIN and senha == PROFESSOR_SENHA:
            session["professor_autenticado"] = True
            return redirect(proxima if proxima.startswith("/") else url_for("criar_feedback"))
        return render_template("login_professor.html", erro="Login ou senha incorretos.", proxima=proxima), 401
    return render_template("login_professor.html", proxima=proxima)


@app.get("/sair-professor")
def sair_professor():
    session.pop("professor_autenticado", None)
    return redirect(url_for("login_professor"))


@app.route("/", methods=["GET", "POST"])
@exigir_professor
def criar_feedback():
    if request.method == "POST":
        turma = request.form.get("turma", "").strip()
        if not turma:
            return render_template("criar.html", erro="Informe o nome da turma."), 400
        try:
            perguntas = carregar_csv(request.files.get("arquivo_csv"))
        except (OSError, UnicodeDecodeError, ValueError) as erro:
            return render_template("criar.html", erro=str(erro)), 400
        codigo = secrets.token_urlsafe(5).replace("-", "").replace("_", "").upper()[:7]
        token = secrets.token_urlsafe(24)
        with conectar() as banco:
            cursor = banco.execute(
                "INSERT INTO sessoes (codigo, turma, token_controle) VALUES (?, ?, ?)",
                (codigo, turma, token),
            )
            for ordem, (tipo, texto, escala) in enumerate(perguntas):
                banco.execute(
                    "INSERT INTO perguntas (sessao_id, ordem, tipo, texto, escala) VALUES (?, ?, ?, ?, ?)",
                    (cursor.lastrowid, ordem, tipo, texto, escala),
                )
        return redirect(url_for("professor", codigo=codigo, token=token))
    return render_template("criar.html")


@app.route("/professor/<codigo>/<token>")
@exigir_professor
def professor(codigo, token):
    sessao = sessao_autorizada(codigo, token)
    if not sessao:
        return render_template("erro.html", mensagem="Link de controle inválido."), 404
    return render_template("professor.html", sessao=sessao, codigo=codigo, token=token)


@app.get("/professor/sessoes")
@exigir_professor
def sessoes_professor():
    with conectar() as banco:
        sessoes = banco.execute("SELECT * FROM sessoes ORDER BY id DESC").fetchall()
    return render_template("sessoes.html", sessoes=sessoes)


@app.post("/api/professor/sessao/<codigo>/<token>/bloquear")
@exigir_professor
def bloquear_sessao(codigo, token):
    sessao = sessao_autorizada(codigo, token)
    if not sessao:
        return jsonify(erro="Sessão não encontrada."), 404
    protegida = 0 if sessao["protegida"] else 1
    with conectar() as banco:
        banco.execute("UPDATE sessoes SET protegida = ? WHERE id = ?", (protegida, sessao["id"]))
    return jsonify(ok=True, protegida=bool(protegida))


@app.post("/api/professor/banco/limpar")
@exigir_professor
def limpar_banco():
    with conectar() as banco:
        resultado = banco.execute("DELETE FROM sessoes WHERE protegida = 0")
    return jsonify(ok=True, removidas=resultado.rowcount)


@app.get("/professor/relatorio-geral")
@exigir_professor
def relatorio_geral():
    return render_template("relatorio_geral.html")


@app.get("/professor/relatorio/<codigo>/<token>")
@exigir_professor
def relatorio_sessao(codigo, token):
    sessao = sessao_autorizada(codigo, token)
    if not sessao:
        return render_template("erro.html", mensagem="Sessão não encontrada."), 404
    return render_template("relatorio_sessao.html", sessao=sessao, codigo=codigo, token=token)


@app.route("/aluno/<codigo>", methods=["GET", "POST"])
def aluno(codigo):
    sessao = buscar_sessao(codigo)
    if not sessao:
        return render_template("erro.html", mensagem="Feedback não encontrado."), 404
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()[:100]
        session["nome_aluno"] = nome  # Opcional e nunca é salvo junto da resposta.
        return redirect(url_for("responder", codigo=codigo))
    return render_template("aluno_entrada.html", sessao=sessao)


@app.route("/aluno/<codigo>/responder")
def responder(codigo):
    sessao = buscar_sessao(codigo)
    if not sessao:
        return render_template("erro.html", mensagem="Feedback não encontrado."), 404
    id_aluno()
    return render_template("aluno.html", sessao=sessao, codigo=codigo)


@app.get("/api/aluno/<codigo>/estado")
def estado_aluno(codigo):
    sessao, pergunta = pergunta_atual(codigo)
    if not sessao:
        return jsonify(erro="Feedback não encontrado"), 404
    if sessao["encerrada"]:
        return jsonify(encerrada=True, respondida=False)
    with conectar() as banco:
        respondida = banco.execute(
            "SELECT 1 FROM respostas WHERE sessao_id = ? AND pergunta_id = ? AND aluno_id = ?",
            (sessao["id"], pergunta["id"], id_aluno()),
        ).fetchone() is not None
    return jsonify(pergunta={"ordem": pergunta["ordem"] + 1, "total": sessao["pergunta_atual"] + 1,
                             "tipo": pergunta["tipo"], "texto": pergunta["texto"], "escala": pergunta["escala"]}, respondida=respondida)


@app.post("/api/aluno/<codigo>/responder")
def registrar_resposta(codigo):
    sessao, pergunta = pergunta_atual(codigo)
    if not sessao or not pergunta or sessao["encerrada"]:
        return jsonify(erro="A sessão não está aceitando respostas."), 400
    dados = request.get_json(silent=True) or {}
    valor = str(dados.get("resposta", "")).strip()
    if pergunta["tipo"] == "nota":
        try:
            if not 0 <= int(valor) <= 10 or str(int(valor)) != valor:
                raise ValueError
        except ValueError:
            return jsonify(erro="Escolha uma nota entre 0 e 10."), 400
    elif not valor or len(valor) > 2000:
        return jsonify(erro="Escreva uma resposta com até 2.000 caracteres."), 400
    try:
        with conectar() as banco:
            banco.execute(
                "INSERT INTO respostas (sessao_id, pergunta_id, aluno_id, valor) VALUES (?, ?, ?, ?)",
                (sessao["id"], pergunta["id"], id_aluno(), valor),
            )
    except sqlite3.IntegrityError:
        return jsonify(erro="Sua resposta para esta pergunta já foi registrada."), 409
    return jsonify(ok=True)


@app.get("/api/professor/<codigo>/<token>/dados")
def dados_professor(codigo, token):
    if not professor_logado():
        return jsonify(erro="Não autenticado"), 401
    sessao = sessao_autorizada(codigo, token)
    if not sessao:
        return jsonify(erro="Não autorizado"), 403
    with conectar() as banco:
        pergunta = banco.execute("SELECT * FROM perguntas WHERE sessao_id = ? AND ordem = ?",
                                 (sessao["id"], sessao["pergunta_atual"])).fetchone()
        conectados = banco.execute("SELECT COUNT(DISTINCT aluno_id) FROM respostas WHERE sessao_id = ?",
                                   (sessao["id"],)).fetchone()[0]
        respostas = banco.execute("SELECT valor FROM respostas WHERE sessao_id = ? AND pergunta_id = ?",
                                  (sessao["id"], pergunta["id"] if pergunta else -1)).fetchall()
    valores = [linha["valor"] for linha in respostas]
    dados = {"turma": sessao["turma"], "encerrada": bool(sessao["encerrada"]),
             "pergunta_atual": sessao["pergunta_atual"] + 1, "total_perguntas": 0,
             "conectados": conectados, "respostas": len(valores), "tipo": None,
             "pergunta": "", "escala": "", "notas": [0] * 11, "media": None, "comentarios": []}
    with conectar() as banco:
        dados["total_perguntas"] = banco.execute("SELECT COUNT(*) FROM perguntas WHERE sessao_id = ?",
                                                  (sessao["id"],)).fetchone()[0]
    if pergunta:
        dados.update(tipo=pergunta["tipo"], pergunta=pergunta["texto"], escala=pergunta["escala"])
        if pergunta["tipo"] == "nota":
            notas_validas = extrair_notas_validas(valores)
            for valor in notas_validas:
                dados["notas"][valor] += 1
            dados["respostas"] = len(notas_validas)
            dados["media"] = round(sum(notas_validas) / len(notas_validas), 2) if notas_validas else None
        else:
            dados["comentarios"] = valores
    return jsonify(dados)


@app.get("/api/professor/<codigo>/<token>/relatorio")
@exigir_professor
def api_relatorio_sessao(codigo, token):
    sessao = sessao_autorizada(codigo, token)
    if not sessao:
        return jsonify(erro="Não autorizado"), 403
    with conectar() as banco:
        perguntas = banco.execute("SELECT * FROM perguntas WHERE sessao_id = ? ORDER BY ordem", (sessao["id"],)).fetchall()
        resultado = []
        todas = []
        for pergunta in perguntas:
            valores = [linha[0] for linha in banco.execute("SELECT valor FROM respostas WHERE pergunta_id = ?", (pergunta["id"],)).fetchall()]
            notas = [0] * 11
            if pergunta["tipo"] == "nota":
                notas_validas = extrair_notas_validas(valores)
                for valor in notas_validas:
                    notas[valor] += 1
                    todas.append(valor)
            else:
                notas_validas = []
            resultado.append({"ordem": pergunta["ordem"] + 1, "tipo": pergunta["tipo"], "pergunta": pergunta["texto"], "escala": pergunta["escala"], "notas": notas, "media": round(sum(notas_validas) / len(notas_validas), 2) if notas_validas else None, "respostas": len(notas_validas) if pergunta["tipo"] == "nota" else len(valores)})
    return jsonify(turma=sessao["turma"], perguntas=resultado, notas_gerais=[todas.count(i) for i in range(11)], media_geral=round(sum(todas) / len(todas), 2) if todas else None)


@app.get("/api/professor/relatorio-geral/dados")
@exigir_professor
def api_relatorio_geral():
    with conectar() as banco:
        linhas = banco.execute("SELECT r.valor FROM respostas r JOIN perguntas p ON p.id = r.pergunta_id WHERE p.tipo = 'nota'").fetchall()
        valores = [int(linha[0]) for linha in linhas]
    return jsonify(notas=[valores.count(i) for i in range(11)], media=round(sum(valores) / len(valores), 2) if valores else None, respostas=len(valores))


@app.post("/api/professor/<codigo>/<token>/proxima")
@exigir_professor
def proxima_pergunta(codigo, token):
    sessao = sessao_autorizada(codigo, token)
    if not sessao or sessao["encerrada"]:
        return jsonify(erro="Sessão encerrada ou não autorizada."), 400
    with conectar() as banco:
        total = banco.execute("SELECT COUNT(*) FROM perguntas WHERE sessao_id = ?", (sessao["id"],)).fetchone()[0]
        if sessao["pergunta_atual"] + 1 >= total:
            return jsonify(erro="Esta é a última pergunta. Encerre o feedback quando terminar."), 400
        banco.execute("UPDATE sessoes SET pergunta_atual = pergunta_atual + 1 WHERE id = ?", (sessao["id"],))
    return jsonify(ok=True)


@app.post("/api/professor/<codigo>/<token>/encerrar")
@exigir_professor
def encerrar(codigo, token):
    sessao = sessao_autorizada(codigo, token)
    if not sessao:
        return jsonify(erro="Não autorizado"), 403
    with conectar() as banco:
        banco.execute("UPDATE sessoes SET encerrada = 1 WHERE id = ?", (sessao["id"],))
    return jsonify(ok=True)


inicializar_banco()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5454, debug=False)
