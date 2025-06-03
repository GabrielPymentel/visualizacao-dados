from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'dados_ambiente.db'  # Renomeei só pra refletir que agora é mais que só temperatura

# 🚀 Cria o banco se não existir
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS dados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura REAL NOT NULL,
            umidade REAL NOT NULL,
            horario DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 🛠 Inicializa ao rodar
init_db()

# 📥 Rota para o ESP32 enviar os dados
@app.route('/enviar', methods=['POST'])
def receber_dados():
    try:
        dados = request.get_json()
        temperatura = dados.get("temperatura")
        umidade = dados.get("umidade")

        if temperatura is not None and umidade is not None:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO dados (temperatura, umidade) VALUES (?, ?)", (temperatura, umidade))
            conn.commit()
            conn.close()
            return jsonify({"status": "sucesso", "temperatura": temperatura, "umidade": umidade}), 200
        else:
            return jsonify({"erro": "Dados incompletos"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ✅ Rota raiz simples
@app.route('/')
def home():
    return "API Flask online e recebendo temperatura e umidade."

# 📊 Rota para visualizar últimos dados
@app.route('/listar')
def listar_dados():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM dados ORDER BY horario DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

# ▶️ Roda o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
