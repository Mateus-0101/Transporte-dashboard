CREATE TABLE viagens (
    id INTEGER PRIMARY KEY,
    rota_id INTEGER NOT NULL REFERENCES rotas(id),
    veiculo_placa TEXT NOT NULL REFERENCES veiculos(placa),
    data DATE NOT NULL,
    turno TEXT NOT NULL,
    tempo_real_min INTEGER NOT NULL,
    passageiros INTEGER NOT NULL
);