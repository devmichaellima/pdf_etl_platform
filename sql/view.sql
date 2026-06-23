-- ========================================
-- INDICADORES GERAIS
-- ========================================

CREATE VIEW vw_indicadores AS
SELECT 
    sum(valor) as faturamento_total,
    count(*) as total_recibos,
    round(avg(valor),2) as ticket_medio,
    max(valor) as maior_faturamento,
    count(distinct cliente) as qtd_clientes,
    PERCENTILE_CONT(0.5)
    WITHIN GROUP (ORDER BY valor) AS mediana
FROM recibos;

-- ========================================
-- ANÁLISE DE CLIENTES
-- ========================================

-- clientes com maior numero de ordens

CREATE VIEW vw_clientes_recorrentes AS
SELECT
    cliente,
    SUM(valor) AS faturamento,
    COUNT(*) AS qtd_ordens
FROM recibos
GROUP BY cliente
HAVING COUNT(*) > 1
ORDER BY qtd_ordens DESC;


-- top 10 clientes por faturamentos

CREATE VIEW vw_top_clientes AS
SELECT 
    cliente,
    sum(valor) as faturamento,
    count(*) as qtd_ordens
FROM recibos
GROUP BY cliente
ORDER BY faturamento DESC
LIMIT 10;

-- ========================================
-- ANÁLISE TEMPORAL
-- ========================================

-- analise por mes

CREATE VIEW vw_analise_mensal AS
SELECT
    DATE_TRUNC('month', data)::date AS mes,
	sum(valor) as faturamento_total,
	count(*) as qtd_ordens,
    round(avg(valor),2) as ticket_medio,
    max(valor) as maior_faturamento,
    count(distinct cliente) as qtd_clientes,
    
	PERCENTILE_CONT(0.5)
    WITHIN GROUP (ORDER BY valor) AS mediana

FROM recibos
GROUP BY mes
ORDER BY mes;


-- analise por dia da semana

CREATE VIEW vw_analise_dia_semana AS
SELECT
	EXTRACT(DOW FROM data) AS dia_semana,
    
	CASE
    WHEN EXTRACT(DOW FROM data) = 0 THEN 'Domingo'
    WHEN EXTRACT(DOW FROM data) = 1 THEN 'Segunda'
    WHEN EXTRACT(DOW FROM data) = 2 THEN 'Terça'
    WHEN EXTRACT(DOW FROM data) = 3 THEN 'Quarta'
    WHEN EXTRACT(DOW FROM data) = 4 THEN 'Quinta'
    WHEN EXTRACT(DOW FROM data) = 5 THEN 'Sexta'
    WHEN EXTRACT(DOW FROM data) = 6 THEN 'Sábado'
END AS nome_dia,

	sum(valor) as faturamento_total,
	count(*) as qtd_ordens,
    round(avg(valor),2) as ticket_medio,
    max(valor) as maior_faturamento,
    count(distinct cliente) as qtd_clientes,
    
	PERCENTILE_CONT(0.5)
    WITHIN GROUP (ORDER BY valor) AS mediana

FROM recibos
GROUP BY dia_semana
ORDER BY dia_semana;

-- ========================================
-- ANALISE POR FAIXA DE PREÇO
-- ========================================

CREATE VIEW vw_faixa_preco AS
SELECT

    CASE

        WHEN valor <= 500
            THEN 'Até R$ 500'

        WHEN valor <= 1000
            THEN 'R$ 501 - R$ 1.000'

        WHEN valor <= 2000
            THEN 'R$ 1.001 - R$ 2.000'

        WHEN valor <= 5000
            THEN 'R$ 2.001 - R$ 5.000'

        ELSE
            'Acima de R$ 5.000'

    END AS faixa_valor,

    COUNT(*) AS qtd_ordens,

    SUM(valor) AS faturamento,

    ROUND(AVG(valor),2) AS ticket_medio,

    ROUND(
        SUM(valor) * 100.0 /
        SUM(SUM(valor)) OVER (),
        2
    ) AS percentual_faturamento,

	    ROUND(
        count(*) * 100.0 /
        sum(count(*)) OVER (),
        2
    ) AS percentual_qtd_ordens

FROM recibos
GROUP BY faixa_valor
ORDER BY qtd_ordens DESC;



