from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def buscar_extrafarma(medicamento):
    resultados = []
    try:
        termo = medicamento.replace(" ", "%20")
        url = f"https://www.extrafarma.com.br/busca?q={termo}"
        
        # Simulando iPhone para pegar a versão mobile que você inspecionou
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        
        resposta = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Usando a classe de container que você localizou
        blocos = soup.find_all('div', class_='extrafarmav2-store-theme-4-x-productPriceContainer')
        
        for bloco in blocos:
            # Pegando o preço com a classe exata que você enviou
            preco_elem = bloco.find('div', class_='extrafarmav2-store-theme-4-x-price')
            preco_texto = preco_elem.get_text().strip() if preco_elem else "R$ --"
            
            # Buscando o link e o nome do produto
            link_elem = bloco.find_parent('a') or bloco.find_previous('a', href=True)
            
            # Lógica de economia: limpando o preço para ordenar do mais barato
            try:
                valor_num = float(preco_texto.replace('R$', '').replace('\xa0', '').replace('.', '').replace(',', '.').strip())
            except:
                valor_num = 9999.0

            nome = link_elem.get('title') if link_elem and link_elem.get('title') else medicamento.upper()
            link_final = "https://www.extrafarma.com.br" + link_elem.get('href') if link_elem else "#"

            resultados.append({
                "farmacia": "Extrafarma",
                "produto": nome,
                "preco": preco_texto,
                "valor": valor_num,
                "link": link_final
            })
            
        return sorted(resultados, key=lambda x: x['valor'])
    except:
        return []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Busca de Remédios - Família Abreu</title>
</head>
<body class="bg-slate-900 text-white p-4">
    <div class="max-w-2xl mx-auto">
        <header class="text-center mb-8">
            <h1 class="text-2xl font-bold text-blue-400">Comparador de Preços 💊</h1>
            <p class="text-slate-400 text-sm">Focado na economia para pais e avós</p>
        </header>

        <form method="POST" class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl mb-6">
            <input type="text" name="remedio" value="{{ remedio }}" placeholder="Qual o remédio? (ex: Dorflex)" required
                   class="w-full bg-slate-900 p-4 rounded-xl border border-slate-700 mb-4 outline-none focus:border-blue-500 text-white">
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 p-4 rounded-xl font-bold">
                Pesquisar Agora
            </button>
        </form>

        <div class="space-y-4">
            {% for item in resultados %}
            <div class="bg-slate-800 p-5 rounded-2xl border border-slate-700 flex justify-between items-center">
                <div>
                    <h3 class="font-semibold text-slate-200">{{ item.produto }}</h3>
                    <p class="text-xs text-blue-400 font-bold">EXTRAFARMA</p>
                </div>
                <div class="text-right">
                    <p class="text-2xl font-mono text-green-400 font-bold">{{ item.preco }}</p>
                    <a href="{{ item.link }}" target="_blank" class="text-xs text-blue-300 underline">Ver no site →</a>
                </div>
            </div>
            {% endfor %}
        </div>
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
