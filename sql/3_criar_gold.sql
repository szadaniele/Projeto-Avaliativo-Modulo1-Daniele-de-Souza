-- Reexecutavel: recria as agregacoes com os dados Silver atuais.

DROP VIEW IF EXISTS gold_visao_pagamentos;
DROP VIEW IF EXISTS gold_visao_trechos;
DROP TABLE IF EXISTS gold_resumo_orgaos;

-- TABELA GOLD: previne multiplicar viagens ao juntar com varios pagamentos.
-- Primeiro soma pagamentos por viagem e depois agrupa por orgao superior.
CREATE TABLE gold_resumo_orgaos AS
SELECT
    v.nome_orgao_superior AS orgao_superior,
    COUNT(*) AS quantidade_viagens,
    SUM(COALESCE(v.valor_total, 0))::NUMERIC(16,2) AS custo_total_viagens,
    SUM(COALESCE(p.total_pagamentos, 0))::NUMERIC(16,2) AS total_pago
FROM silver_viagem v
LEFT JOIN (
    SELECT id_viagem, SUM(COALESCE(valor, 0)) AS total_pagamentos
    FROM silver_pagamento
    GROUP BY id_viagem
) p ON v.id_viagem = p.id_viagem
GROUP BY v.nome_orgao_superior;

-- VIEW GOLD: valores do pagamento agrupados por orgao pagador e tipo.
CREATE VIEW gold_visao_pagamentos AS
SELECT
    COALESCE(NULLIF(p.nome_orgao_pagador, ''), v.nome_orgao_superior)
        AS orgao_pagador,
    p.tipo_pagamento,
    COUNT(*) AS quantidade_pagamentos,
    SUM(COALESCE(p.valor, 0))::NUMERIC(16,2) AS valor_total_pago,
    ROUND(AVG(p.valor), 2) AS valor_medio
FROM silver_pagamento p
JOIN silver_viagem v ON p.id_viagem = v.id_viagem
GROUP BY 1, 2;

-- VIEW GOLD: quantidade de trechos por transporte e UF, ligada a viagens.
CREATE VIEW gold_visao_trechos AS
SELECT
    COALESCE(t.meio_transporte, 'Sem informação') AS meio_transporte,
    COALESCE(t.destino_uf, 'Sem informação') AS destino_uf,
    COUNT(*) AS quantidade_trechos
FROM silver_trecho t
JOIN silver_viagem v ON t.id_viagem = v.id_viagem
GROUP BY 1, 2;
