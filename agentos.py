import os
from agno.os import AgentOS
from app.agents.agente_produtos import agente_especialista
from fastapi.responses import HTMLResponse
from fastapi import Request
from urllib.parse import quote

agent = agente_especialista

agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7777))
    
    agent_os.serve(
        "agentos:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True
    )