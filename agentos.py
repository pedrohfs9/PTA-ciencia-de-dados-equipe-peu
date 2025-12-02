from agno.os import AgentOS
from app.agents.agente_produtos import agente_especialista

from fastapi.responses import HTMLResponse
from fastapi import Request
from urllib.parse import quote

agent = agente_especialista

from agno.os import AgentOS

agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agentos:app", reload=True)