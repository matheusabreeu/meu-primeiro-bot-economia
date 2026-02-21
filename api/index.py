from flask import Flask, render_template_string, request

app = Flask(__name__)

def gerar_links_busca(remedio):
    termo = remedio.replace(" ", "+")
    # URLs de busca padrão das farmácias que você utiliza
    return [
        {"loja": "Extrafarma", "url": f"https://www.extrafarma.com.br/busca?q={termo}", "cor": "blue"},
        {"loja": "Pague Menos", "url": f"https://www.paguemenos.com.br/{termo}", "cor": "red"},
        {"loja": "Drogasil", "url": f"https://www.drogasil.com.br/search?w={termo}", "cor": "green"},
        {"loja": "Drogarias Globo", "url": f"https://www.drogariasglobo.com.br/busca?q={termo}", "cor": "orange"}
    ]

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
    <div class="max-w-xl mx-auto">
        <header class="text-center mb-8">
            <h1 class="text-3xl font-bold text-blue-400">Medicamento Barato 💊</h1>
            <p class="text-slate-400 text-sm">Central de Links para Pais e Avós</p>
        </header>

        <form method="POST" class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-2xl mb-8">
            <label class="block text-sm font-medium text-slate-400 mb-2">Digite o nome do remédio:</label>
            <input type="text" name="remedio" value="{{ remedio }}" placeholder="Ex: Dorflex" required
                   class="w-full bg-slate-900 p-4 rounded-xl border border-slate-700 mb-4 outline-none focus:border-blue-500 text-white text-lg">
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 p-4 rounded-xl font-bold transition text-lg">
                Gerar Links de Comparação
            </button>
        </form>

        {% if links %}
        <div class="grid grid-cols-1 gap-4">
            <h2 class="text-lg font-semibold text-slate-300 px-2">Pesquisar em:</h2>
            {% for link in links %}
            <a href="{{ link.url }}" target="_blank" 
               class="bg-slate-800 p-5 rounded-2xl border border-slate-700 flex justify-between items-center hover:bg-slate-700 transition group">
                <span class="font-bold text-lg text-{{ link.cor }}-400">{{ link.loja }}</span>
                <span class="text-slate-500 group-hover:text-white">Abrir busca →</span>
            </a>
            {% endfor %}
        </div>
        <div class="mt-8 p-4 bg-blue-900/20 border border-blue-800 rounded-xl text-sm text-blue-300">
            <strong>Dica de Economia:</strong> Clique em cada link acima. As páginas abrirão com os preços atualizados de São Luís. Assim, você garante o menor preço sem erro de sistema.
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    links = []
    remedio = ""
    if request.method == 'POST':
        remedio = request.form.get('remedio')
        links = gerar_links_busca(remedio)
    return render_template_string(HTML_TEMPLATE, links=links, remedio=remedio)
