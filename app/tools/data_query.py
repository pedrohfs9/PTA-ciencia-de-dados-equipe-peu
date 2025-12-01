from agno.tool import tool, ToolParameter
from typing import Literal, Optional, List
import pandas as pd
import os

# --- 1. DEFINIÇÃO DOS CAMINHOS DOS ARQUIVOS ---

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
FILES = {
    'produtos': os.path.join(BASE_DIR, 'produtos.csv'),
    'itens_pedidos': os.path.join(BASE_DIR, 'itens_pedidos.csv'),
    'pedidos': os.path.join(BASE_DIR, 'pedidos.csv'),
    'vendedores': os.path.join(BASE_DIR, 'vendedores.csv'),
}

# --- 2. FUNÇÃO TOOL (@agno.tool) ---

@tool(
    name="consulta_data_warehouse",
    description=(
        "Use esta ferramenta para buscar dados numéricos e exatos, E TAMBÉM para responder "
        "perguntas de análise complexa, como 'qual é o produto mais vendido', 'o peso de um produto', "
        "ou 'qual vendedor tem mais vendas'. A consulta exige a união de múltiplas tabelas."
    ),
)
def buscar_dados_exatos(
    query_type: Literal["product_detail", "top_selling", "top_seller", "product_dimensions"] = ToolParameter(
        description="O tipo de análise ou dado exato solicitado (detalhe de produto, mais vendido, melhor vendedor, ou dimensão/peso)."
    ),
    product_id: Optional[str] = ToolParameter(
        description="O ID único do produto a ser consultado (necessário apenas para dimensões e peso)."
    ),
) -> str:
    """
    Busca dados exatos ou realiza análises de vendas/ranking unindo as quatro tabelas do DW.
    """
    print(f"Iniciando análise complexa: {query_type}...")
    
    try:
        # Carrega todas as tabelas
        df_produtos = pd.read_csv(FILES['produtos'])
        df_itens_pedidos = pd.read_csv(FILES['itens_pedidos'])
        df_pedidos = pd.read_csv(FILES['pedidos'])
        df_vendedores = pd.read_csv(FILES['vendedores'])
        
    except FileNotFoundError:
        return "❌ Erro: Um ou mais arquivos de dados (CSV) não foram encontrados na pasta 'data'."
    except Exception as e:
        return f"❌ Erro ao carregar dados: {e}"
    
    # --- 3. CRIAÇÃO DA TABELA MESTRE (JOIN) ---
    
    # 1. Unir Itens de Pedidos com Produtos (pela product_id)
    df_merged = pd.merge(df_itens_pedidos, df_produtos, on='product_id', how='left')
    
    # 2. Unir com Pedidos (pela order_id)
    df_merged = pd.merge(df_merged, df_pedidos, on='order_id', how='left')
    
    # 3. Unir com Vendedores (pela seller_id)
    df_final = pd.merge(df_merged, df_vendedores, on='seller_id', how='left')
    
    # --- 4. EXECUÇÃO DA CONSULTA BASEADA NO query_type ---
    
    if query_type == "product_dimensions" or query_type == "product_detail":
        if not product_id:
            return "Erro: O product_id é obrigatório para consultas de dimensão."
        
        # Filtra pelo ID do produto
        resultado = df_final[df_final['product_id'] == product_id][['product_weight_g', 'product_length_cm']].iloc[0]
        
        return f"Peso (g): {resultado['product_weight_g']}, Comprimento (cm): {resultado['product_length_cm']}"

    elif query_type == "top_selling":
        # Conta a frequência de cada produto nos itens de pedidos
        top_produtos = df_final['product_id'].value_counts().nlargest(1).index[0]
        return f"O produto mais vendido (pelo ID) é: {top_produtos}."

    elif query_type == "top_seller":
        # Agrupa pelo ID do vendedor e soma o número de vendas/itens
        top_vendedor = df_final['seller_id'].value_counts().nlargest(1).index[0]
        return f"O vendedor com o maior número de itens vendidos é: {top_vendedor}."

    return "Tipo de consulta não reconhecido ou dados insuficientes."
