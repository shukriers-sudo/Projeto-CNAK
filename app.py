from flask import Flask, render_template, request, redirect, url_for
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)
DB = {
    "users": DB_DIR / "users.json",
    "modules": DB_DIR / "modules.json",
    "environments": DB_DIR / "environments.json",
}

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
    DB[key].write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")

def next_id(data):
    return max([item.get("id", 0) for item in data], default=0) + 1

@app.route("/")
def dashboard():
    return render_template(
        "index.html",
        total_users=len(load_data("users")),
        total_modules=len(load_data("modules")),
        total_environments=len(load_data("environments"))
    )

@app.route("/usuarios", methods=["GET", "POST"])
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
def excluir_usuario(item_id):
    save_data("users", [item for item in load_data("users") if item.get("id") != item_id])
    return redirect(url_for("usuarios"))

@app.route("/modulos", methods=["GET", "POST"])
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
def excluir_modulo(item_id):
    save_data("modules", [item for item in load_data("modules") if item.get("id") != item_id])
    return redirect(url_for("modulos"))

@app.route("/ambientes", methods=["GET", "POST"])
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
def excluir_ambiente(item_id):
    save_data("environments", [item for item in load_data("environments") if item.get("id") != item_id])
    return redirect(url_for("ambientes"))

if __name__ == "__main__":
    app.run(debug=True)
