from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def buscar_extrafarma(medicamento):
    resultados = []
    try:
        # Formata o termo de busca para a URL
        termo = medicamento.replace(" ", "%20")
        url = f"https://www.extrafarma.com.br/busca?q={termo}"
        
        # Simula um navegador mobile (conforme você viu na emulação)
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        
        resposta = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Localiza todos os blocos de produtos usando a classe que você identificou
        blocos = soup.find_all('div', class_='extrafarmav2-store-theme-4-x-productPriceContainer')
        
        for bloco in blocos:
            # 1. Extração do Preço
            preco_elem = bloco.find('div', class_='extrafarmav2-store-theme-4-x-price')
            preco_texto = preco_elem.get_text().strip() if preco_elem else "Consulte"
            
            # 2. Extração do Link e Nome
            # Buscamos o link 'a' que envolve ou está próximo ao bloco de preço
            link_elem = bloco.find_parent('a') or bloco.find_previous('a', href=True)
            
            # Lógica para converter o preço em número e permitir ordenação
            try:
                # Remove R$, espaços e ajusta vírgula para ponto
                valor_num = float(preco_texto.replace('R$', '').replace('\xa0', '').replace('.', '').replace(',', '.').strip())
            except:
                valor_num = 9999.0 

            # Tenta pegar o nome do remédio no título do link
            nome_produto = link_elem.get('title') if link_elem and link_elem.get('title') else medicamento.capitalize()
            link_final = "https://www.extrafarma.com.br" + link_elem.get('href') if link_elem else "#"

            resultados.append({
                "farmacia": "Extrafarma",
                "produto": nome_produto,
                "preco": preco_texto,
                "valor": valor_num,
                "link": link_final
            })
            
        # Ordenação: Menor preço primeiro ($P_{1} < P_{2} < ... < P_{n}$)
        return sorted(resultados, key=lambda x: x['valor'])
        
    except Exception as e:
        return []

# Interface Visual (HTML + CSS Tailwind)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Busca Medicamentos</title>
</head>
<body class="bg-slate-900 text-white p-4">
    <div class="max-w-2xl mx-auto">
        <header class="text-center mb-8">
            <h1 class="text-2xl font-bold text-blue-400">Comparador de Preços 💊</h1>
            <p class="text-slate-400 text-sm italic">Economia para a família</p>
        </header>

        <form method="POST" class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl mb-6">
            <input type="text" name="remedio" value="{{ remedio }}" placeholder="Digite o remédio (ex: Dorflex)" required
                   class="w-full bg-slate-900 p-4 rounded-xl border border-slate-700 mb-4 outline-none focus:border-blue-500 transition text-white">
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 p-4 rounded-xl font-bold transition">
                Pesquisar na Extrafarma
            </button>
        </form>

        {% if resultados %}
        <div class="space-y-4">
            {% for item in resultados %}
            <div class="bg-slate-800 p-5 rounded-2xl border border-slate-700 flex justify-between items-center hover:border-blue-500 transition">
                <div class="flex-1 pr-4">
                    <h3 class="font-semibold text-slate-200 leading-tight">{{ item.produto }}</h3>
                    <p class="text-xs text-blue-400 uppercase font-bold mt-1">{{ item.farmacia }}</p>
                </div>
                <div class="text-right">
                    <p class="text-2xl font-mono text-green-400 font-bold">{{ item.preco }}</p>
                    <a href="{{ item.link }}" target="_blank" 
                       class="inline-block mt-2 text-xs bg-blue-900/40 text-blue-300 border border-blue-800 px-4 py-2 rounded-lg hover:bg-blue-800 transition">
                       Comprar Agora →
                    </a>
                </div>
            </div>
            {% endfor %}
        </div>
        {% elif remedio %}
        <div class="bg-red-900/20 border border-red-900 text-red-400 p-4 rounded-xl text-center">
            Nenhum resultado para "{{ remedio }}". Tente outro nome.
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    resultados = []
    remedio = ""
    if request.method == 'POST':
        remedio = request.form.get('remedio')
        resultados = buscar_extrafarma(remedio)
    return render_template_string(HTML_TEMPLATE, resultados=resultados, remedio=remedio)
