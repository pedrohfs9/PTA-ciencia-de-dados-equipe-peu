from agno.tools import tool, ToolParameter
from typing import Literal, Optional

@tool(
    name="consulta_data_warehouse",
    description=(
        "Esta ferramenta é EXCLUSIVA para buscar dados numéricos e "
        "exatos sobre um produto, como peso em gramas (product_weight_g) "
        "e comprimento em centímetros (product_length_cm), usando o ID do produto."
    ),
)
def buscar_dados_exatos(
    # O LLM (Gemini) precisa fornecer o ID
    product_id: str = ToolParameter(description="O ID único do produto a ser consultado."),
    dado_solicitado: Literal["weight", "length"] = ToolParameter(
        description="O tipo de dado exato que o usuário solicitou (peso ou comprimento)."
    ),
) -> Optional[float]:
    """
    Simula a consulta ao Data Warehouse (DW) para retornar dados exatos do produto.
    """
    print(f"Buscando {dado_solicitado} para o Produto ID: {product_id} no DW...")

    # --- LÓGICA DE CONEXÃO E CONSULTA AO DW ---
    
    # Exemplo simples (Apenas ilustrativo):
    if product_id == "ABC1234":
        if dado_solicitado == "weight":
            return 1200.0  # Retorna o peso (numérico)
        if dado_solicitado == "length":
            return 30.5   # Retorna o comprimento (numérico)
        
    return None