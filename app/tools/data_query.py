import os
import pandas as pd
import duckdb
from agno.tools import tool

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

def carregar_dataframes():
    """Carrega os CSVs para DataFrames do Pandas"""
    return {
        'produtos': pd.read_csv(os.path.join(BASE_DIR, 'produtos.csv')),
        'itens': pd.read_csv(os.path.join(BASE_DIR, 'itens_pedidos.csv')),
        'pedidos': pd.read_csv(os.path.join(BASE_DIR, 'pedidos.csv')),
        'vendedores': pd.read_csv(os.path.join(BASE_DIR, 'vendedores.csv'))
    }

dfs = carregar_dataframes()
df_produtos = dfs['produtos']
df_itens = dfs['itens']
df_pedidos = dfs['pedidos']
df_vendedores = dfs['vendedores']

@tool(
    name="executar_sql_data_warehouse",
    description=(
        "Executa uma consulta SQL completa nos dados da empresa. "
        "Tabelas disponíveis: 'df_produtos', 'df_itens', 'df_pedidos', 'df_vendedores'."
    )
)
def executar_query_analitica(query_sql: str):
    """
    Executa SQL DuckDB garantindo que as tabelas estejam visíveis.
    """
    try:

        con = duckdb.connect(database=':memory:')
        
        con.register('df_produtos', df_produtos)
        con.register('df_itens', df_itens)
        con.register('df_pedidos', df_pedidos)
        con.register('df_vendedores', df_vendedores)

        if "drop" in query_sql.lower() or "delete" in query_sql.lower():
            return "Erro: Apenas consultas de leitura (SELECT) são permitidas."

        resultado = con.execute(query_sql).df()
        
        if resultado.empty:
            return "A consulta rodou com sucesso, mas não retornou nenhuma linha (resultado vazio)."
            
        return resultado.to_string(index=False)

    except Exception as e:
        try:
            cols = con.execute("DESCRIBE df_produtos").df().to_string()
            return f"Erro SQL: {str(e)} \n\nColunas disponíveis na tabela df_produtos: \n{cols}"
        except:
            return f"Erro Crítico SQL: {str(e)}"