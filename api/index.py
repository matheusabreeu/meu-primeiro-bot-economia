from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def buscar_extrafarma(medicamento):
    resultados = []
    try:
        termo = medicamento.replace(" ", "%20")
        url = f"https://www.extrafarma.com.br/busca?q={termo}"
        
        # Cabeçalho mais "humano" para evitar ser bloqueado
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        
        sessao = requests.Session()
        resposta = sessao.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # TÁTICA: Buscamos por qualquer elemento que contenha "Price" ou "Container" na classe
        # Isso ajuda se o site mudar o número do "theme"
        blocos = soup.find_all('div', class_=lambda x: x and 'productPriceContainer' in x)
        
        if not blocos:
            # Se falhar, tentamos buscar por qualquer div que tenha a palavra 'price'
            blocos = soup.find_all('div', class_=lambda x: x and 'price' in x.lower())

        for bloco in blocos:
            # Busca o texto que tem o R$
            texto_bloco = bloco.get_text().strip()
            if "R$" in texto_bloco:
                # Extrai apenas o valor monetário usando expressão regular
                match_preco = re.search(r'R\$\s?\d+,\d{2}', texto_bloco)
                preco_final = match_preco.group() if match_preco else "Consulte"
                
                # Busca o link próximo a esse preço
                link_elem = bloco.find_parent('a') or bloco.find_previous('a', href=True)
                
                # Lógica de Economia: Tratamento do valor para ordenação
                try:
                    valor_limpo = preco_final.replace('R$', '').replace('.', '').replace(',', '.').strip()
                    valor_num = float(valor_limpo)
                except:
                    valor_num = 9999.0

                link_final = "https://www.extrafarma.com.br" + link_elem.get('href') if link_elem else "#"
                nome = link_elem.get('title') if link_elem and link_elem.get('title') else medicamento.upper()

                resultados.append({
                    "farmacia": "Extrafarma",
                    "produto": nome,
                    "preco": preco_final,
                    "valor": valor_num,
                    "link": link_final
                })
        
        # Ordenação por menor preço (Eficiência de Mercado)
        return sorted(resultados, key=lambda x: x['valor'])
    except Exception as e:
        print(f"Erro técnico: {e}")
        return []

# Interface Visual Mantida
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Busca de Medicamentos - Família Abreu</title>
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
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 p-4 rounded-xl font-bold transition">
                Pesquisar na Extrafarma
            </button>
        </form>

        <div class="space-y-4">
            {% for item in resultados %}
            <div class="bg-slate-800 p-5 rounded-2xl border border-slate-700 flex justify-between items-center hover:border-blue-500 transition">
                <div>
                    <h3 class="font-semibold text-slate-200">{{ item.produto }}</h3>
                    <p class="text-xs text-blue-400 font-bold uppercase">{{ item.farmacia }}</p>
                </div>
                <div class="text-right">
                    <p class="text-2xl font-mono text-green-400 font-bold">{{ item.preco }}</p>
                    <a href="{{ item.link }}" target="_blank" class="text-xs text-blue-300 underline">Comprar no Site →</a>
                </div>
            </div>
            {% endfor %}
            {% if remedio and not resultados %}
            <div class="bg-amber-900/20 border border-amber-700 text-amber-400 p-4 rounded-xl text-center">
                O site da farmácia não respondeu com dados. Tentando nova estratégia...
            </div>
            {% endif %}
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
