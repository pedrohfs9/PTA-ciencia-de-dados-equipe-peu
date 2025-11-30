from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.tavily import TavilyTools
from agno.db.sqlite import SqliteDb
from app.knowledge.base_pdfs import base_conhecimento

load_dotenv()
agent_storage: str = "tmp/agents.db"

agente_especialista = Agent(
    name="Agente Especialista",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[TavilyTools()],
    instructions=(
        "Você é um especialista em produtos e utiliza os PDFs técnicos da "
        "base de conhecimento para responder perguntas relacionadas."
    ),
    knowledge=base_conhecimento,
    search_knowledge=True,
    read_chat_history=True,
    db=SqliteDb(db_file=agent_storage),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)
