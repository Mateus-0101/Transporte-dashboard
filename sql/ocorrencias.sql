CREATE TABLE ocorrencias (
    id INTEGER PRIMARY KEY,
    viagem_id INTEGER NOT NULL REFERENCES viagens(id),
    tipo TEXT NOT NULL
);