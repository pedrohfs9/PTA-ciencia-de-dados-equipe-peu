# 1. Imports essenciais
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.tavily import TavilyTools
from agno.storage.sqlite import SqliteStorage
from dotenv import load_dotenv

# Carrega as chaves do .env
load_dotenv() 

# 2. IMPORTAÇÃO DA BASE DE CONHECIMENTO (Cérebro do Agente)
from app.knowledge.base_pdfs import base_conhecimento
agent_storage: str = "tmp/agents.db"

# 3. Definição do Agente
agente_especialista = Agent(
    name="Especialista de Produtos",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[TavilyTools()],
    instructions="Você é um especialista em produtos e deve usar a base de conhecimento para responder a todas as perguntas sobre documentos técnicos.",
    knowledge=base_conhecimento,
    search_knowledge=True,
    
    # 1. Ativa a persistência (guarda o histórico no ficheiro .db)
    storage=SqliteStorage(table_name="agente_especialista", db_file=agent_storage),
    
    # 2. Envia o histórico da conversa para o modelo
    add_history_to_messages=True,
    
    # 3. Define quantas mensagens anteriores o modelo "lembra"
    num_history_responses=5,
    
    # 4. Formatação e Utilitários
    markdown=True,
    add_datetime_to_instructions=True,
)