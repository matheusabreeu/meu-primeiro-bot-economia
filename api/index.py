from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Simulação de raspagem (cada farmácia tem uma estrutura de site diferente)
def buscar_preco(farmacia, medicamento):
    # Nota: Na vida real, cada farmácia exige um código de raspagem específico
    # Aqui vamos simular o retorno para você ver a interface funcionando
    precos_exemplo = {
        "Drogasil": 15.90,
        "Pague Menos": 14.50,
        "Extrafarma": 16.20,
        "Drogarias Globo": 13.80
    }
    import random
    valor = precos_exemplo.get(farmacia, 20.00) + random.uniform(-2, 2)
    return round(valor, 2)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Busca Medicamentos - Família Abreu</title>
</head>
<body class="bg-slate-900 text-white p-6">
    <div class="max-w-2xl mx-auto">
        <h1 class="text-3xl font-bold text-blue-400 mb-6">Comparador de Preços 💊</h1>
        
        <form method="POST" class="bg-slate-800 p-6 rounded-xl border border-slate-700 mb-8">
            <div class="mb-4">
                <label class="block text-sm font-medium mb-2">Nome do Medicamento:</label>
                <input type="text" name="remedio" placeholder="Ex: Dorflex" required
                       class="w-full bg-slate-700 p-3 rounded-lg border border-slate-600 focus:outline-none focus:border-blue-500">
            </div>

            <div class="mb-6">
                <label class="block text-sm font-medium mb-2">Selecione as Farmácias:</label>
                <div class="grid grid-cols-2 gap-2 text-sm">
                    <label><input type="checkbox" name="lojas" value="Extrafarma" checked> Extrafarma</label>
                    <label><input type="checkbox" name="lojas" value="Pague Menos" checked> Pague Menos</label>
                    <label><input type="checkbox" name="lojas" value="Drogarias Globo" checked> Drogarias Globo</label>
                    <label><input type="checkbox" name="lojas" value="Drogasil" checked> Drogasil</label>
                </div>
            </div>

            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 p-3 rounded-lg font-bold transition">
                Pesquisar Menor Preço
            </button>
        </form>

        {% if resultados %}
        <div class="bg-slate-800 rounded-xl overflow-hidden border border-slate-700">
            <table class="w-full text-left">
                <thead class="bg-slate-700 text-slate-300">
                    <tr>
                        <th class="p-4">Farmácia</th>
                        <th class="p-4">Preço</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in resultados %}
                    <tr class="border-t border-slate-700 hover:bg-slate-700/50">
                        <td class="p-4 font-semibold">{{ item.farmacia }}</td>
                        <td class="p-4 text-green-400 font-mono text-lg italic">R$ {{ item.preco }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <p class="text-xs text-slate-500 mt-4 italic text-center text-red-500">
          Resultados ordenados do mais barato para o mais caro.
        </p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    resultados = []
    if request.method == 'POST':
        remedio = request.form.get('remedio')
        lojas_selecionadas = request.form.getlist('lojas')
        
        for loja in lojas_selecionadas:
            preco = buscar_preco(loja, remedio)
            resultados.append({"farmacia": loja, "preco": preco})
        
        # Lógica de Economia: Ordenar do menor para o maior preço
        resultados = sorted(resultados, key=lambda x: x['preco'])

    return render_template_string(HTML_TEMPLATE, resultados=resultados)
