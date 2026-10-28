import pandas as pd
from sqlalchemy import create_engine, text

# Conexão com o banco local
engine = create_engine("postgresql+psycopg2:///transporte")

TABELAS = ["rotas", "veiculos", "viagens", "ocorrencias"]


def limpar_tabelas():
    """Esvazia as tabelas para poder rodar o script mais de uma vez."""
    with engine.begin() as conexao:
        conexao.execute(text("TRUNCATE ocorrencias, viagens, veiculos, rotas"))


def carregar_tabela(nome):
    """Lê data/<nome>.csv e insere na tabela <nome>."""
    df = pd.read_csv(f"data/{nome}.csv")
    df.to_sql(nome, engine, if_exists="append", index=False)
    print(f"{nome}: {len(df)} linhas carregadas")


if __name__ == "__main__":
    limpar_tabelas()
    for nome in TABELAS:
        carregar_tabela(nome)