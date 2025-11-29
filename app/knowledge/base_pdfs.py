from dotenv import load_dotenv
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.google import GeminiEmbedder

load_dotenv()

# 1. Configuração do Banco de Dados Vetorial
vetor_db = LanceDb(
    table_name="base_produtos",
    uri="tmp/lancedb",
    search_type=SearchType.vector,
    embedder=GeminiEmbedder(),
)

# 2. Criação da Base de Conhecimento
base_conhecimento = PDFKnowledgeBase(
    path="data/produtos",
    vector_db=vetor_db,
)

def carregar_conhecimento():
    """
    Lê os PDFs e salva no banco.
    """
    print("Iniciando leitura dos PDFs...")
    try:
        base_conhecimento.load(recreate=True)
        print("✅ Sucesso! Base de conhecimento criada e salva em tmp/lancedb.")
    except Exception as e:
        print(f"❌ Ocorreu um erro durante a leitura: {e}")

if __name__ == "__main__":
    carregar_conhecimento()