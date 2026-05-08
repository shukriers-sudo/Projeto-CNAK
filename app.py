from flask import Flask, render_template, request, redirect, url_for, session
import json
from pathlib import Path
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "argos_cnak_modulo_01_seguro"

# =========================
# CONFIGURAÇÕES
# =========================

USUARIO_PADRAO = "admin"
SENHA_PADRAO = "1234"

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

DB = {
    "users": DB_DIR / "users.json",
    "modules": DB_DIR / "modules.json",
    "environments": DB_DIR / "environments.json",
    "equipamentos": DB_DIR / "equipamentos.json",
    "distribuicao": DB_DIR / "distribuicao.json",
}

# =========================
# FUNÇÕES AUXILIARES
# =========================

def load_data(key):
    path = DB[key]

    if not path.exists():
        path.write_text("[]", encoding="utf-8")

    try:
        content = path.read_text(encoding="utf-8").strip()
        return json.loads(content) if content else []
    except json.JSONDecodeError:
        return []


def save_data(key, data):
    DB[key].write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )


def next_id(data):
    return max([item.get("id", 0) for item in data], default=0) + 1


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logado"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    erro = None

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()

        if usuario == USUARIO_PADRAO and senha == SENHA_PADRAO:

            session["logado"] = True
            session["usuario"] = usuario

            return redirect(url_for("dashboard"))

        else:
            erro = "Usuário ou senha inválidos."

    return render_template("login.html", erro=erro)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# =========================
# DASHBOARD
# =========================

@app.route("/")
@login_required
def dashboard():

    return render_template(
        "index.html",
        total_users=len(load_data("users")),
        total_modules=len(load_data("modules")),
        total_environments=len(load_data("environments")),
        total_equipamentos=len(load_data("equipamentos"))
    )

# =========================
# USUÁRIOS
# =========================

@app.route("/usuarios", methods=["GET", "POST"])
@login_required
def usuarios():

    items = load_data("users")

    if request.method == "POST":

        items.append({
            "id": next_id(items),
            "nome": request.form.get("nome", "").strip(),
            "email": request.form.get("email", "").strip(),
            "perfil": request.form.get("perfil", "").strip(),
            "status": request.form.get("status", "Ativo"),
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
        })

        save_data("users", items)

        return redirect(url_for("usuarios"))

    return render_template("usuarios.html", items=items)


@app.route("/usuarios/excluir/<int:item_id>")
@login_required
def excluir_usuario(item_id):

    save_data(
        "users",
        [item for item in load_data("users") if item.get("id") != item_id]
    )

    return redirect(url_for("usuarios"))

# =========================
# MÓDULOS
# =========================

@app.route("/modulos", methods=["GET", "POST"])
@login_required
def modulos():

    items = load_data("modules")

    if request.method == "POST":

        items.append({
            "id": next_id(items),
            "nome": request.form.get("nome", "").strip(),
            "descricao": request.form.get("descricao", "").strip(),
            "nivel_acesso": request.form.get("nivel_acesso", "").strip(),
            "status": request.form.get("status", "Ativo"),
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
        })

        save_data("modules", items)

        return redirect(url_for("modulos"))

    return render_template("modulos.html", items=items)


@app.route("/modulos/excluir/<int:item_id>")
@login_required
def excluir_modulo(item_id):

    save_data(
        "modules",
        [item for item in load_data("modules") if item.get("id") != item_id]
    )

    return redirect(url_for("modulos"))

# =========================
# AMBIENTES
# =========================

@app.route("/ambientes", methods=["GET", "POST"])
@login_required
def ambientes():

    items = load_data("environments")

    if request.method == "POST":

        items.append({
            "id": next_id(items),
            "nome": request.form.get("nome", "").strip(),
            "tipo": request.form.get("tipo", "").strip(),
            "localizacao": request.form.get("localizacao", "").strip(),
            "nivel_risco": request.form.get("nivel_risco", "").strip(),
            "status": request.form.get("status", "Ativo"),
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
        })

        save_data("environments", items)

        return redirect(url_for("ambientes"))

    return render_template("ambientes.html", items=items)


@app.route("/ambientes/excluir/<int:item_id>")
@login_required
def excluir_ambiente(item_id):

    save_data(
        "environments",
        [item for item in load_data("environments") if item.get("id") != item_id]
    )

    return redirect(url_for("ambientes"))

# =========================
# EQUIPAMENTOS
# =========================

@app.route("/equipamentos", methods=["GET", "POST"])
@login_required
def equipamentos():

    items = load_data("equipamentos")

    if request.method == "POST":

        items.append({
            "id": next_id(items),
            "nome": request.form.get("nome", "").strip(),
            "tipo": request.form.get("tipo", "").strip(),
            "patrimonio": request.form.get("patrimonio", "").strip(),
            "status": request.form.get("status", "Ativo"),
            "ambiente": request.form.get("ambiente", "").strip(),
            "responsavel": request.form.get("responsavel", "").strip(),
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
        })

        save_data("equipamentos", items)

        return redirect(url_for("equipamentos"))

    return render_template("equipamentos.html", items=items)


@app.route("/equipamentos/excluir/<int:item_id>")
@login_required
def excluir_equipamento(item_id):

    save_data(
        "equipamentos",
        [item for item in load_data("equipamentos") if item.get("id") != item_id]
    )

    return redirect(url_for("equipamentos"))

# =========================
# DISTRIBUIÇÃO
# =========================

@app.route("/distribuicao", methods=["GET", "POST"])
@login_required
def distribuicao():

    items = load_data("distribuicao")

    if request.method == "POST":

        items.append({
            "id": next_id(items),
            "equipamento": request.form.get("equipamento", "").strip(),
            "ambiente": request.form.get("ambiente", "").strip(),
            "responsavel": request.form.get("responsavel", "").strip(),
            "status": request.form.get("status", "Operacional"),
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
        })

        save_data("distribuicao", items)

        return redirect(url_for("distribuicao"))

    return render_template("distribuicao.html", items=items)


@app.route("/distribuicao/excluir/<int:item_id>")
@login_required
def excluir_distribuicao(item_id):

    save_data(
        "distribuicao",
        [item for item in load_data("distribuicao") if item.get("id") != item_id]
    )

    return redirect(url_for("distribuicao"))


# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    app.run(debug=True)