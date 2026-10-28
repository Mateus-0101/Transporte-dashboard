import random
import pandas as pd
import string

random.seed(2026)  

REGIOES = ["Plano Piloto", "Taguatinga", "Ceilândia", "Samambaia", "Gama", "Sobradinho"]

def gerar_rotas():
    linhas = []
    for i in range(12):
        linhas.append({
            "id": i + 1,
            "nome": f"Rota {i + 1:02d}",
            "regiao": REGIOES[i // 2],
            "tempo_previsto_min": random.randint(30, 70),
        })
    return pd.DataFrame(linhas)

rotas = gerar_rotas()
rotas.to_csv("data/rotas.csv", index=False)

def gerar_placa():
    letras = "".join(random.choices(string.ascii_uppercase, k=3))
    numero1 = random.choice(string.digits)
    letra2 = random.choice(string.ascii_uppercase)
    numeros2 = "".join(random.choices(string.digits, k=2))
    return letras + numero1 + letra2 + numeros2

def gerar_veiculos():
    carros = []
    usadas = set()
    for i in range(15):
        placa = gerar_placa()
        while placa in usadas:
            placa = gerar_placa()
        usadas.add(placa)
        carros.append({
            "placa": placa,
            "capacidade": random.randint(40, 60),
        })
    return pd.DataFrame(carros)

def gerar_viagens(rotas, veiculos):
    dias = pd.bdate_range("2026-07-27", "2026-10-23")   # só dias úteis
    chuva = {dia: random.random() < 0.09 for dia in dias}   # ~9% dos dias com chuva
    atraso_base = {r["id"]: random.uniform(1, 8) for _, r in rotas.iterrows()}
    capacidade = dict(zip(veiculos["placa"], veiculos["capacidade"]))
    placas = list(capacidade.keys())

    linhas = []
    id_viagem = 1
    for dia in dias:
        for _, rota in rotas.iterrows():
            for turno in ["Manhã", "Tarde"]:
                atraso = atraso_base[rota["id"]]
                if chuva[dia]:
                    atraso = atraso * 1.8      # a chuva multiplica o atraso (ex.: 1.8)
                if turno == "Tarde":
                    atraso = atraso + 1.5      # a tarde atrasa um pouco mais (ex.: 1.5)
                atraso = max(0, round(random.gauss(atraso, 3)))

                placa = random.choice(placas)
                passageiros = int(capacidade[placa] * random.uniform(0.5, 1.0))

                linhas.append({
                    "id": id_viagem,
                    "rota_id": rota["id"],
                    "veiculo_placa": placa,
                    "data": dia.strftime("%Y-%m-%d"),
                    "turno": turno,
                    "tempo_real_min": rota["tempo_previsto_min"] + atraso,     # tempo previsto da rota + atraso
                    "passageiros": passageiros,
                })
                id_viagem += 1
    return pd.DataFrame(linhas)

TIPOS = ["Trânsito intenso", "Falha mecânica", "Ausência de monitor", "Desvio de rota"]

def gerar_ocorrencias(viagens):
    quantidade = int(len(viagens) * 0.05)
    ids_sorteados = random.sample(list(viagens["id"]), k=quantidade)

    linhas = []
    for i, viagem_id in enumerate(ids_sorteados, start=1):
        linhas.append({
            "id": i,
            "viagem_id": viagem_id,
            "tipo": random.choice(TIPOS),
        })
    return pd.DataFrame(linhas)

if __name__ == "__main__":
    rotas = gerar_rotas()
    veiculos = gerar_veiculos()
    viagens = gerar_viagens(rotas, veiculos)
    ocorrencias = gerar_ocorrencias(viagens)

    rotas.to_csv("data/rotas.csv", index=False)
    veiculos.to_csv("data/veiculos.csv", index=False)
    viagens.to_csv("data/viagens.csv", index=False)
    ocorrencias.to_csv("data/ocorrencias.csv", index=False)
    print("Dados gerados em data/")