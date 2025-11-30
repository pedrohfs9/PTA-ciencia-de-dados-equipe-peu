# 1. Imports essenciais
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv

# Carrega as chaves do .env
load_dotenv() 

# 2. IMPORTAÇÃO DA BASE DE CONHECIMENTO (Cérebro do Agente)
from app.knowledge.base_pdfs import base_conhecimento

# 3. Definição do Agente
agente_especialista = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    tools=[TavilyTools()],
    instructions="Você é um especialista em produtos e deve usar a base de conhecimento para responder a todas as perguntas sobre documentos técnicos.",
    knowledge=base_conhecimento,
    search_knowledge=True,
    read_chat_history=True
)