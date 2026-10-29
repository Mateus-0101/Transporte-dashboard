# Painel de Operações de Transporte público

Projeto de análise de dados de ponta a ponta: modelagem de um banco **PostgreSQL**, geração de dados fictícios em **Python**, consultas em **SQL**, análise em **Jupyter** e um dashboard interativo em **Streamlit**.

**Painel online:** https://transporte-dashboard.streamlit.app

![Painel de Operações de Transporte público](imagens/painel.png)

> **Aviso:** todos os dados são fictícios, gerados por código para demonstração. Eles não têm relação com nenhuma operação real.

## Contexto

Acompanhar uma operação de transporte público exige responder perguntas do dia a dia: quais rotas atrasam mais, em que turno, em quais regiões e que tipos de ocorrência são mais comuns. Este projeto simula essa operação e mostra como transformar os registros de viagens em indicadores e recomendações.

Uma viagem é considerada **pontual** quando o atraso (tempo real menos tempo previsto da rota) é de até 5 minutos.

## O que o painel mostra

- Indicadores: total de viagens, pontualidade e atraso médio.
- Atraso médio por rota.
- Evolução semanal da pontualidade.
- Ocorrências por tipo.
- Ranking de rotas por atraso.
- Filtros por região, turno e período.

## Dados simulados

| Tabela | Conteúdo |
|---|---|
| `rotas` | 12 rotas em 6 regiões do DF, com tempo de percurso previsto |
| `veiculos` | 15 ônibus, identificados pela placa, com capacidade |
| `viagens` | 1.560 viagens (65 dias úteis, 2 turnos por dia, de 27/07/2026 a 23/10/2026) |
| `ocorrencias` | 78 ocorrências de 4 tipos, ligadas às viagens |

Os atrasos seguem regras simples (rota, turno e dias de chuva simulados), e o gerador usa semente fixa, então os mesmos dados são produzidos a cada execução.

## Tecnologias

Python 3.12, pandas, SQLAlchemy, psycopg2, PostgreSQL, SQL, matplotlib, Jupyter e Streamlit.

## Estrutura do projeto

```
transporte-dashboard/
├── app.py                  # dashboard Streamlit
├── data/                   # CSVs gerados (rotas, veiculos, viagens, ocorrencias)
├── notebooks/
│   └── analise.ipynb       # análise com gráficos e conclusões
├── sql/
│   ├── schema.sql          # cria as tabelas (chama os demais arquivos)
│   ├── rotas.sql
│   ├── veiculos.sql
│   ├── viagens.sql
│   ├── ocorrencias.sql
│   └── consultas.sql       # consultas de análise
├── src/
│   ├── gerar_dados.py      # gera os dados fictícios em CSV
│   └── carregar_banco.py   # carrega os CSVs no PostgreSQL
├── requirements.txt        # dependências do painel publicado
└── requirements-dev.txt    # dependências completas (notebook e banco)
```

## Como rodar

O painel publicado lê os CSVs da pasta `data/`. O banco PostgreSQL é usado nas consultas SQL e no notebook.

**1. Clonar e preparar o ambiente**
```bash
git clone https://github.com/Mateus-0101/transporte-dashboard.git
cd transporte-dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

**2. Só o painel (sem banco)**
```bash
streamlit run app.py
```

**3. Banco de dados, consultas e notebook** (requer PostgreSQL instalado)
```bash
createdb transporte
psql -d transporte -f sql/schema.sql
python src/gerar_dados.py
python src/carregar_banco.py
psql -d transporte -f sql/consultas.sql
```
Depois, abra `notebooks/analise.ipynb` no VS Code ou no Jupyter, usando o ambiente `.venv`.

Se o `createdb` reclamar que o usuário não existe, crie um perfil com `sudo -u postgres createuser --createdb $USER`.

## Principais achados

- A Rota 07 tem o maior atraso médio (cerca de 8 minutos), e as rotas variam de aproximadamente 3 a 8 minutos.
- A pontualidade semanal oscila entre cerca de 52% e 68%, com quedas nas semanas de chuva simulada.
- As ocorrências se distribuem de forma parecida entre os quatro tipos, com leve predominância de desvio de rota.

## O que aprendi

- Modelar um banco relacional, com chaves primárias e estrangeiras.
- Gerar dados fictícios reproduzíveis com Python e pandas.
- Escrever consultas SQL com JOIN, GROUP BY e funções de agregação.
- Analisar dados em notebook e transformar números em recomendações.
- Construir e publicar um dashboard interativo.
- Organizar um projeto com Git, ambiente virtual e documentação.

## Próximos passos

- Adicionar testes automatizados para a geração e a carga dos dados.
- Incluir previsão de atrasos com machine learning.
- Mostrar a ocupação dos veículos no painel.
- Conectar o painel a um banco hospedado.

## Autor

**Mateus Antunes Dias Rodrigues** | Engenheiro da Computação

[Portfólio](https://mateus-0101.github.io) | [LinkedIn](https://www.linkedin.com/in/mateus-antunes-1a7704234) | [GitHub](https://github.com/Mateus-0101)
