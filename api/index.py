from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def buscar_extrafarma(medicamento):
    try:
        # 1. URL de busca da Extrafarma
        url = f"https://www.extrafarma.com.br/busca?q={medicamento}"
        
        # 2. Cabeçalho para simular um navegador real (evita bloqueios)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        resposta = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # 3. Localizar os produtos na página
        # Nota: Sites de farmácia mudam as "classes" do HTML com frequência.
        # Geralmente os preços estão em tags de 'span' ou 'div'.
        produtos = []
        
        # Exemplo de lógica para encontrar o primeiro item da lista
        # Vamos procurar por elementos que geralmente contêm preços (ex: R$)
        for item in soup.find_all('span'):
            texto = item.get_text()
            if "R$" in texto and "," in texto:
                # Limpamos o texto para pegar apenas o número
                preco_limpo = texto.replace("R$", "").strip()
                return preco_limpo
        
        return "Não encontrado"
    except Exception as e:
        return f"Erro na busca"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Busca Extrafarma - Família Abreu</title>
</head>
<body class="bg-slate-900 text-white p-6">
    <div class="max-w-xl mx-auto">
        <header class="mb-10 text-center">
            <h1 class="text-3xl font-bold text-blue-400">Pesquisa Extrafarma 💊</h1>
            <p class="text-slate-400">Focado em economia para a família</p>
        </header>

        <form method="POST" class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl">
            <label class="block text-sm font-medium text-slate-400 mb-2">Qual medicamento procura?</label>
            <div class="flex gap-2">
                <input type="text" name="remedio" placeholder="Ex: Dorflex" required
                       class="flex-1 bg-slate-900 p-4 rounded-xl border border-slate-700 focus:border-blue-500 outline-none transition">
                <button type="submit" class="bg-blue-600 hover:bg-blue-700 px-6 rounded-xl font-bold transition">
                    Buscar
                </button>
            </div>
        </form>

        {% if resultado %}
        <div class="mt-8 animate-bounce-in">
            <div class="bg-slate-800 p-6 rounded-2xl border-l-4 border-green-500">
                <div class="flex justify-between items-center">
                    <div>
                        <p class="text-sm text-slate-400 uppercase">Menor preço na Extrafarma</p>
                        <h2 class="text-xl font-bold italic">{{ remedio }}</h2>
                    </div>
                    <div class="text-right">
                        <p class="text-3xl font-mono text-green-400">R$ {{ resultado }}</p>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    resultado = None
    remedio = ""
    if request.method == 'POST':
        remedio = request.form.get('remedio')
        resultado = buscar_extrafarma(remedio)
    
    return render_template_string(HTML_TEMPLATE, resultado=resultado, remedio=remedio)
