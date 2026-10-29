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

@st.cache_data
def carregar_ocorrencias():
    return pd.read_sql("SELECT * FROM ocorrencias", engine)

# 1. Dados
viagens = carregar()
data_inicial = viagens["data"].min().date()
data_final = viagens["data"].max().date()

# 2. Título
st.title("Painel de Operações de Transporte Público")
st.caption("Dados fictícios para demonstração")

# 3. Filtros (barra lateral)
regiao = st.sidebar.selectbox("Região", ["Todas"] + sorted(viagens["regiao"].unique()))
if regiao != "Todas":
    viagens = viagens[viagens["regiao"] == regiao]

turnos = st.sidebar.multiselect("Turno", ["Manhã", "Tarde"], default=["Manhã", "Tarde"])
viagens = viagens[viagens["turno"].isin(turnos)]

periodo = st.sidebar.date_input("Período", value=(data_inicial, data_final))
if len(periodo) == 2:
    inicio, fim = periodo
    viagens = viagens[viagens["data"].between(pd.Timestamp(inicio), pd.Timestamp(fim))]

# 4. Proteção: se os filtros não deixaram nenhuma viagem, para aqui
if viagens.empty:
    st.warning("Nenhuma viagem para os filtros escolhidos.")
    st.stop()

# 5. Indicadores
col1, col2, col3 = st.columns(3)
col1.metric("Viagens", len(viagens))
col2.metric("Pontualidade", f"{viagens['pontual'].mean() * 100:.1f}%")
col3.metric("Atraso médio", f"{viagens['atraso'].mean():.1f} min")

# 6. Gráficos
semanal = viagens.set_index("data").resample("W")["pontual"].mean() * 100

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Atraso médio por rota")
    st.bar_chart(viagens.groupby("rota")["atraso"].mean())
with col_b:
    st.subheader("Pontualidade semanal (%)")
    if len(semanal) < 2:
        st.info("Escolha um período maior para ver a evolução semanal.")
    else:
        st.line_chart(semanal)

ocorrencias = carregar_ocorrencias()
ocorrencias = ocorrencias[ocorrencias["viagem_id"].isin(viagens["id"])]

st.subheader("Ocorrências por tipo")
if ocorrencias.empty:
    st.info("Nenhuma ocorrência para os filtros escolhidos.")
else:
    st.bar_chart(ocorrencias["tipo"].value_counts())