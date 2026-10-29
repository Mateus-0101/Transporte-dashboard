import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title="Painel de Transporte", layout="wide")
engine = create_engine("postgresql+psycopg2:///transporte")


@st.cache_data
def carregar():
    df = pd.read_sql("""
        SELECT v.*, r.nome AS rota, r.regiao,
               v.tempo_real_min - r.tempo_previsto_min AS atraso
        FROM viagens v
        JOIN rotas r ON r.id = v.rota_id
    """, engine)
    df["data"] = pd.to_datetime(df["data"])
    df["pontual"] = df["atraso"] <= 5
    return df


viagens = carregar()

st.title("Painel de Operações de Transporte Escolar")
st.caption("Dados fictícios para demonstração")

regiao = st.sidebar.selectbox("Região", ["Todas"] + sorted(viagens["regiao"].unique()))
if regiao != "Todas":
    viagens = viagens[viagens["regiao"] == regiao]

col1, col2, col3 = st.columns(3)
col1.metric("Viagens", len(viagens))
col2.metric("Pontualidade", f"{______:.1f}%")      # média de "pontual" vezes 100
col3.metric("Atraso médio", f"{______:.1f} min")    # média de "atraso"

st.subheader("Atraso médio por rota")
st.bar_chart(______)  