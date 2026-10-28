SELECT
    COUNT(*) AS viagens,
    ROUND(100.0 * AVG(CASE WHEN v.tempo_real_min - r.tempo_previsto_min <= 5
                           THEN 1 ELSE 0 END), 1) AS pontualidade_pct
FROM viagens v
JOIN rotas r ON r.id = v.rota_id;

SELECT r.nome, r.regiao,
       ROUND(AVG(v.tempo_real_min - r.tempo_previsto_min), 1) AS atraso_medio
FROM viagens v
JOIN rotas r ON r.id = v.rota_id
GROUP BY r.nome, r.regiao
ORDER BY atraso_medio DESC;