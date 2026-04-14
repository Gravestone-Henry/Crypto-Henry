from flask import Flask, render_template, jsonify
from flask_cors import CORS # Opcional, mas ajuda a evitar erros de permissão
import requests

app = Flask(__name__)
CORS(app) # Permite que o front-end acesse a API sem bloqueios

# LOGICA DE BUSCA DE DADOS
def fetch_binance_price(symbol="BTCUSDT"):
    try:
        # Endpoint público da Binance
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Verifica se a API respondeu com sucesso
        data = response.json()
        
        return {
            "symbol": data["symbol"],
            "price": float(data["price"])
        }
    except Exception as e:
        return {"error": str(e)}

# ROTAS (ROUTING)

# Rota que o navegador acessa
@app.route('/')
def index():
    # O Flask procura automaticamente na pasta 'templates/'
    return render_template('index.html')

# Rota que o JavaScript do seu HTML vai chamar
@app.route('/api/price')
def get_price():
    price_data = fetch_binance_price()
    return jsonify(price_data)

if __name__ == '__main__':
    # Rode o servidor em modo Debug para facilitar o desenvolvimento
    app.run(debug=True, port=5000)