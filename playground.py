from agno.playground import Playground, serve_playground_app
from app.agents.agente_produtos import agente_especialista

app = Playground(agents=[agente_especialista]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)