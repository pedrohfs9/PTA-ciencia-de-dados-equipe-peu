import os
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
    caminho_alvo = "data/produtos"
    documentos_totais = []
    
    try:
        if not os.path.exists(caminho_alvo):
            print(f"⚠️ O caminho '{caminho_alvo}' não foi encontrado.")
            return

        leitor = PDFReader()

        if os.path.isdir(caminho_alvo):
            print(f"📂 Lendo diretório: {caminho_alvo}")
            for arquivo in os.listdir(caminho_alvo):
                if arquivo.lower().endswith(".pdf"):
                    caminho_completo = os.path.join(caminho_alvo, arquivo)
                    print(f"   📖 Lendo: {arquivo}")
                    try:
                        docs = leitor.read(caminho_completo)
                        documentos_totais.extend(docs)
                    except Exception as e_arquivo:
                        print(f"   ❌ Erro ao ler {arquivo}: {e_arquivo}")
        else:
            print(f"📄 Lendo arquivo único: {caminho_alvo}")
            documentos_totais = leitor.read(caminho_alvo)
        
        if documentos_totais:
            vetor_db.insert(documents=documentos_totais, content_hash=None)
            print(f"✅ Sucesso! {len(documentos_totais)} partes de documentos carregados em tmp/lancedb.")
        else:
            print("⚠️ Nenhum PDF válido foi encontrado ou lido.")
            
    except Exception as e:
        print(f"❌ Erro crítico ao processar: {e}")

if __name__ == "__main__":
    carregar_conhecimento()