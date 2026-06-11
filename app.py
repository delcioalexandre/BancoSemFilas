from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pymysql
import bcrypt
import os
from datetime import datetime

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# ─────────────────────────────────────────
# CONFIGURAÇÃO DA BASE DE DADOS
# ─────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER",     "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "db":       os.getenv("DB_NAME",     "bancosemfilas"),
    "charset":  "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}

def get_db():
    """Abre uma ligação à base de dados."""
    return pymysql.connect(**DB_CONFIG)


# ─────────────────────────────────────────
# SERVIR PÁGINAS HTML
# ─────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/<path:filename>")
def serve_html(filename):
    if filename.endswith(".html"):
        return send_from_directory("templates", filename)
    return send_from_directory("static", filename)


# ─────────────────────────────────────────
# AUTH — LOGIN
# ─────────────────────────────────────────
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    tipo = data.get("tipo")          # "cliente" | "funcionario"

    conn = get_db()
    try:
        with conn.cursor() as cur:
            if tipo == "cliente":
                cur.execute(
                    "SELECT id, nome, senha_hash FROM clientes WHERE email = %s",
                    (data.get("email"),)
                )
                user = cur.fetchone()
                if user and bcrypt.checkpw(data.get("senha", "").encode(), user["senha_hash"].encode()):
                    return jsonify({"ok": True, "tipo": "cliente",
                                    "id": user["id"], "nome": user["nome"]})
                return jsonify({"ok": False, "erro": "Email ou senha incorretos."}), 401

            elif tipo == "funcionario":
                cur.execute(
                    "SELECT id, nome, senha_hash FROM funcionarios WHERE username = %s",
                    (data.get("username"),)
                )
                user = cur.fetchone()
                if user and bcrypt.checkpw(data.get("senha", "").encode(), user["senha_hash"].encode()):
                    return jsonify({"ok": True, "tipo": "funcionario",
                                    "id": user["id"], "nome": user["nome"]})
                return jsonify({"ok": False, "erro": "ID ou senha incorretos."}), 401

            return jsonify({"ok": False, "erro": "Tipo inválido."}), 400
    finally:
        conn.close()


# ─────────────────────────────────────────
# MARCAÇÕES — CRIAR
# ─────────────────────────────────────────
@app.route("/api/marcacoes", methods=["POST"])
def criar_marcacao():
    d = request.get_json()
    campos = ["nome", "bi", "telefone", "email", "banco", "agencia",
              "servico", "data", "horario"]
    for c in campos:
        if not d.get(c):
            return jsonify({"ok": False, "erro": f"Campo '{c}' obrigatório."}), 400

    conn = get_db()
    try:
        with conn.cursor() as cur:
            # Verifica disponibilidade de horário
            cur.execute(
                """SELECT id FROM marcacoes
                   WHERE banco=%s AND agencia=%s AND data=%s AND horario=%s
                     AND estado != 'Cancelado'""",
                (d["banco"], d["agencia"], d["data"], d["horario"])
            )
            if cur.fetchone():
                return jsonify({"ok": False, "erro": "Horário indisponível para esta agência."}), 409

            # Gera senha sequencial (ex: A011)
            cur.execute("SELECT COUNT(*) AS total FROM marcacoes")
            total = cur.fetchone()["total"]
            senha = "A" + str(total + 1).zfill(3)

            cur.execute(
                """INSERT INTO marcacoes
                   (senha, nome, bi, telefone, email, banco, agencia, servico, data, horario, estado)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'Aguardar')""",
                (senha, d["nome"], d["bi"], d["telefone"], d["email"],
                 d["banco"], d["agencia"], d["servico"], d["data"], d["horario"])
            )
            conn.commit()
            return jsonify({"ok": True, "senha": senha}), 201
    finally:
        conn.close()


# ─────────────────────────────────────────
# MARCAÇÕES — LISTAR (dashboard)
# ─────────────────────────────────────────
@app.route("/api/marcacoes", methods=["GET"])
def listar_marcacoes():
    data_filtro = request.args.get("data")       # YYYY-MM-DD
    estado      = request.args.get("estado", "")
    pesquisa    = request.args.get("q", "")

    conn = get_db()
    try:
        with conn.cursor() as cur:
            sql    = "SELECT * FROM marcacoes WHERE 1=1"
            params = []

            if data_filtro:
                sql += " AND data = %s"; params.append(data_filtro)
            if estado:
                sql += " AND estado = %s"; params.append(estado)
            if pesquisa:
                sql += " AND (nome LIKE %s OR senha LIKE %s)"
                params += [f"%{pesquisa}%", f"%{pesquisa}%"]

            sql += " ORDER BY horario ASC"
            cur.execute(sql, params)
            rows = cur.fetchall()

            # Converte date para string
            for r in rows:
                if isinstance(r.get("data"), datetime):
                    r["data"] = r["data"].strftime("%Y-%m-%d")
                elif hasattr(r.get("data"), "isoformat"):
                    r["data"] = r["data"].isoformat()

            return jsonify(rows)
    finally:
        conn.close()


# ─────────────────────────────────────────
# MARCAÇÕES — ATUALIZAR ESTADO
# ─────────────────────────────────────────
@app.route("/api/marcacoes/<int:mid>", methods=["PATCH"])
def atualizar_estado(mid):
    d      = request.get_json()
    estado = d.get("estado")
    if estado not in ("Aguardar", "Atendido", "Cancelado"):
        return jsonify({"ok": False, "erro": "Estado inválido."}), 400

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE marcacoes SET estado=%s WHERE id=%s", (estado, mid))
            conn.commit()
            return jsonify({"ok": True})
    finally:
        conn.close()


# ─────────────────────────────────────────
# ESTATÍSTICAS (dashboard cards)
# ─────────────────────────────────────────
@app.route("/api/estatisticas", methods=["GET"])
def estatisticas():
    data_filtro = request.args.get("data", datetime.today().strftime("%Y-%m-%d"))
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS t FROM marcacoes WHERE data=%s", (data_filtro,))
            total = cur.fetchone()["t"]

            cur.execute("SELECT COUNT(*) AS t FROM marcacoes WHERE data=%s AND estado='Aguardar'",
                        (data_filtro,))
            aguardar = cur.fetchone()["t"]

            cur.execute("SELECT COUNT(*) AS t FROM marcacoes WHERE data=%s AND estado='Atendido'",
                        (data_filtro,))
            atendidos = cur.fetchone()["t"]

            return jsonify({
                "total":     total,
                "senhas":    total,
                "aguardar":  aguardar,
                "atendidos": atendidos,
            })
    finally:
        conn.close()


# ─────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
