from agno.playground import Playground, serve_playground_app
from fastapi import Request
from fastapi.responses import HTMLResponse
from urllib.parse import quote
import os

# 1. IMPORTAÇÃO DO AGENTE
from app.agents.agente_produtos import agente_especialista

# 2. Configuração do Playground 
playground = Playground(agents=[agente_especialista])

# Obtém a aplicação FastAPI
app = playground.get_app()

# 3. Rota da Página Inicial (Para facilitar a conexão)
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    host = request.url.hostname or "localhost"
    port = request.url.port or 7777
    
    endpoint = f"{host}:{port}"
    
    # Cria a URL para o site da Agno
    encoded_endpoint = quote(f"http://{endpoint}/v1")
    playground_url = f"https://app.agno.com/playground?endpoint={encoded_endpoint}"

    return f"""
    <!doctype html>
    <html lang="pt-br">
      <head>
        <meta charset="utf-8" />
        <title>Agente Local</title>
        <style>
          body {{
            font-family: sans-serif; background: #0f172a; color: #f8fafc;
            display: grid; place-items: center; min-height: 100vh; margin: 0;
          }}
          .card {{
            background: #1e293b; padding: 2rem; border-radius: 1rem;
            text-align: center; border: 1px solid #334155;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
          }}
          a.button {{
            display: inline-block; margin-top: 1rem; padding: 0.8rem 1.5rem;
            background: #38bdf8; color: #0f172a; text-decoration: none;
            border-radius: 0.5rem; font-weight: bold;
          }}
          code {{ background: #000; padding: 0.2rem 0.4rem; border-radius: 0.3rem; }}
        </style>
      </head>
      <body>
        <div class="card">
          <h1>Playground Rodando 🚀</h1>
          <p>Seu endpoint local é: <code>http://{endpoint}/v1</code></p>
          <a class="button" href="{playground_url}" target="_blank">Abrir Interface do Chat</a>
        </div>
      </body>
    </html>
    """

# 4. Inicialização
if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True, port=7777)