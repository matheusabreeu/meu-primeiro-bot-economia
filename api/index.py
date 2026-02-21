from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def buscar_remedios(medicamento):
    resultados = []
    try:
        # Busca no agregador Consulta Remédios
        termo = medicamento.replace(" ", "%20")
        url = f"https://consultaremedios.com.br/busca?termo={termo}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        resposta = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Localiza os blocos de produtos
        produtos = soup.find_all('div', class_='product-block')
        
        for p in produtos:
            nome = p.find('a', class_='product-block__title')
            preco = p.find('div', class_='product-block__price')
            link = nome['href'] if nome else "#"
            
            if nome and preco:
                texto_preco = preco.get_text().strip()
                # Limpeza para ordenação
                try:
                    valor_num = float(texto_preco.split('R$')[-1].replace('.', '').replace(',', '.').strip())
                except:
                    valor_num = 9999.0

                resultados.append({
                    "produto": nome.get_text().strip(),
                    "preco": texto_preco,
                    "valor": valor_num,
                    "link": f"https://consultaremedios.com.br{link}"
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
    <title>Busca de Medicamentos</title>
</head>
<body class="bg-slate-900 text-white p-4">
    <div class="max-w-2xl mx-auto">
        <header class="text-center mb-8">
            <h1 class="text-2xl font-bold text-blue-400">Comparador de Preços 💊</h1>
            <p class="text-slate-400 text-sm">Busca em várias farmácias simultaneamente</p>
        </header>

        <form method="POST" class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl mb-6">
            <input type="text" name="remedio" value="{{ remedio }}" placeholder="Qual o remédio? (ex: Dorflex)" required
                   class="w-full bg-slate-900 p-4 rounded-xl border border-slate-700 mb-4 outline-none focus:border-blue-500 text-white">
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 p-4 rounded-xl font-bold">
                Pesquisar Menor Preço
            </button>
        </form>

        <div class="space-y-4">
            {% for item in resultados %}
            <div class="bg-slate-800 p-5 rounded-2xl border border-slate-700 flex justify-between items-center">
                <div class="flex-1 pr-4">
                    <h3 class="font-semibold text-slate-200 text-sm">{{ item.produto }}</h3>
                </div>
                <div class="text-right">
                    <p class="text-xl font-mono text-green-400 font-bold">{{ item.preco }}</p>
                    <a href="{{ item.link }}" target="_blank" class="text-xs text-blue-300 underline">Ver ofertas →</a>
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
        resultados = buscar_remedios(remedio)
    return render_template_string(HTML_TEMPLATE, resultados=resultados, remedio=remedio)
