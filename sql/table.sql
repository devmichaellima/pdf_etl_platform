-- ========================================
-- CRIACAO DA TABELA RECIBOS
-- ========================================

CREATE TABLE recibos (
    numero_recibo VARCHAR(5) UNIQUE,
    cliente VARCHAR(50),
    valor NUMERIC(10,2),
    data DATE,
    arquivo_origem VARCHAR(200),
    data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);