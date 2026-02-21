from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    dados = {
        "usuario": "Matheus Ferreira de Abreu",
        "status": "Online",
        "setor": "Ciências Econômicas - UFMA",
        "mensagem": "Bem-vindo à minha primeira API de automação!"
    }
    return jsonify(dados)

@app.route('/indicadores')
def indicadores():
    # Aqui você poderia futuramente buscar dados reais do IBGE ou Banco Central
    return jsonify({
        "inflacao_mensal": "0.42%",
        "selic": "11.25%",
        "localizacao": "Maranhão"
    })
