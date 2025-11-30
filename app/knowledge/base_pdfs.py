from dotenv import load_dotenv
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.reader.pdf_reader import PDFReader

load_dotenv()

vetor_db = LanceDb(
    table_name="base_produtos",
    uri="tmp/lancedb",
    search_type=SearchType.vector,
    embedder=GeminiEmbedder(),
)

base_conhecimento = Knowledge(
    vector_db=vetor_db,
)

def carregar_conhecimento():
    print("Iniciando leitura dos PDFs...")
    try:
        leitor = PDFReader()
        documentos = leitor.read("data/produtos") 
        
        if documentos:
            base_conhecimento.load_documents(documentos, recreate=True)
            print(f"✅ Sucesso! {len(documentos)} documentos carregados em tmp/lancedb.")
        else:
            print("⚠️ A pasta data/produtos parece vazia.")
            
    except Exception as e:
        print(f"❌ Erro ao carregar PDFs: {e}")

if __name__ == "__main__":
    carregar_conhecimento()