from flask import Flask, render_template_string

app = Flask(__name__)

# Este é o modelo visual da sua página (HTML + CSS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Dashboard Econômico - Matheus Abreu</title>
</head>
<body class="bg-slate-900 text-white font-sans">
    <div class="min-h-screen flex flex-col items-center justify-center p-6">
        
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-slate-700 w-full max-w-md">
            <h1 class="text-2xl font-bold text-blue-400 mb-2">Central de Automação</h1>
            <p class="text-slate-400 mb-6">Matheus Ferreira de Abreu | UFMA</p>
            
            <div class="space-y-4">
                <div class="flex justify-between items-center bg-slate-700 p-4 rounded-lg">
                    <span>Status do Servidor:</span>
                    <span class="text-green-400 font-bold">● Online</span>
                </div>

                <h2 class="text-lg font-semibold mt-4 text-slate-300">Indicadores Econômicos</h2>
                
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-slate-900 p-4 rounded-lg border border-slate-700">
                        <p class="text-xs text-slate-500 uppercase">Selic</p>
                        <p class="text-xl font-mono text-yellow-500">11.25%</p>
                    </div>
                    <div class="bg-slate-900 p-4 rounded-lg border border-slate-700">
                        <p class="text-xs text-slate-500 uppercase">Inflação</p>
                        <p class="text-xl font-mono text-red-500">0.42%</p>
                    </div>
                </div>
            </div>

            <footer class="mt-8 text-center text-xs text-slate-500">
                Desenvolvido para estudos de Ciências Econômicas
            </footer>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Agora ele retorna o template visual em vez do JSON bruto
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/dados')
def api_dados():
    # Mantemos uma rota de dados caso você queira usar em outro robô futuramente
    return {"status": "Online", "usuario": "Matheus Abreu"}
