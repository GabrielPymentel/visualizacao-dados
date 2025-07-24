from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'dados_ambiente.db'

# 🚀 Cria o banco se não existir ou adapta a estrutura
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS dados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura_ar REAL,
            umidade_ar REAL,
            umidade_solo REAL,
            chuva INTEGER,
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

        temperatura_ar = dados.get("temperatura_ar")
        umidade_ar = dados.get("umidade_ar")
        umidade_solo = dados.get("umidade_solo")
        chuva = dados.get("chuva")  # 1 = está chovendo | 0 = seco

        # Aqui a gente deixa flexível: pelo menos um dado deve ser enviado
        if any(v is not None for v in [temperatura_ar, umidade_ar, umidade_solo, chuva]):
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("""
                INSERT INTO dados (temperatura_ar, umidade_ar, umidade_solo, chuva)
                VALUES (?, ?, ?, ?)
            """, (temperatura_ar, umidade_ar, umidade_solo, chuva))
            conn.commit()
            conn.close()
            return jsonify({
                "status": "sucesso",
                "temperatura_ar": temperatura_ar,
                "umidade_ar": umidade_ar,
                "umidade_solo": umidade_solo,
                "chuva": chuva
            }), 200
        else:
            return jsonify({"erro": "Nenhum dado foi enviado"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ✅ Rota raiz simples
@app.route('/')
def home():
    return "API Flask online e recebendo dados ambientais."

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
