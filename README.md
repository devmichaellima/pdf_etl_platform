# Tekar PDF Intelligence

## Sobre o Projeto

O **Tekar PDF Intelligence** é uma ferramenta desenvolvida para automatizar a extração de dados de recibos em PDF utilizados na operação de um Auto Center.

Atualmente, os pedidos são registrados em um aplicativo externo que gera um PDF para cada atendimento realizado. O objetivo deste projeto é transformar esses documentos em dados estruturados, permitindo análises, geração de relatórios e futuras integrações com bancos de dados e automações.

A solução foi construída utilizando Python e Streamlit, permitindo que usuários façam upload de múltiplos PDFs, extraiam informações automaticamente e gerem arquivos CSV prontos para análise.

---

## Problema de Negócio

O processo manual de consultar recibos individualmente apresenta limitações para:

* Consolidar informações de vendas;
* Acompanhar faturamento;
* Identificar clientes recorrentes;
* Gerar indicadores operacionais;
* Alimentar sistemas de Business Intelligence;
* Automatizar processos futuros.

Este projeto resolve esse problema transformando documentos PDF em dados estruturados e utilizáveis.

---

## Objetivos do Projeto

* Automatizar a leitura de recibos em PDF;
* Extrair informações relevantes dos documentos;
* Padronizar e tratar os dados coletados;
* Gerar arquivos CSV para análise;
* Disponibilizar indicadores em dashboard interativo;
* Criar uma base preparada para futuras integrações com banco de dados e automações.

---

## Tecnologias Utilizadas

### Python

Linguagem principal utilizada para todo o processamento da aplicação.

### Streamlit

Responsável pela interface web da aplicação.

Utilizado para:

* Upload de arquivos;
* Exibição de tabelas;
* Indicadores;
* Dashboard;
* Download de relatórios.

### PDFPlumber

Biblioteca utilizada para leitura e extração de texto dos arquivos PDF.

### Pandas

Biblioteca utilizada para:

* Criação de DataFrames;
* Limpeza de dados;
* Padronização de informações;
* Geração de arquivos CSV;
* Cálculo de indicadores.

### DateParser

Utilizado para conversão automática de datas em português para objetos datetime.

### Regex (re)

Utilizado para identificar padrões dentro dos documentos PDF e extrair informações específicas.

### Plotly

Biblioteca utilizada para construção dos gráficos do dashboard.

---

## Fluxo da Aplicação

```text
PDFs
  ↓
Upload no Streamlit
  ↓
Extração de Texto (PDFPlumber)
  ↓
Extração de Campos (Regex)
  ↓
Transformação dos Dados (Pandas)
  ↓
DataFrame
  ↓
Geração de CSV
  ↓
Dashboard e Indicadores
```

---

## Estrutura do Projeto

```text
autocenter-pdf-intelligence/
│
├── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── exports/
│
├── src/
│   ├── extractors/
│   │   └── pdf_extractor.py
│   │
│   ├── transformers/
│   │   └── pedido_transformer.py
│   │
│   ├── dashboards/
│   │   └── pedido_dashboard.py
│   │
│   └── utils/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Funcionalidades Implementadas

### Extração de PDFs

* Upload múltiplo de arquivos PDF;
* Leitura automática dos documentos;
* Extração do texto bruto.

### Processamento de Dados

Extração das informações:

* Número do recibo;
* Data;
* Cliente;
* Valor da venda.

### Transformação dos Dados

* Conversão de datas;
* Conversão de valores monetários;
* Padronização de nomes;
* Criação de DataFrame para análise.

### Exportação

* Geração automática de CSV;
* Download do relatório pela interface.

### Dashboard

Indicadores principais:

* Total de recibos processados;
* Faturamento total;
* Ticket médio;
* Maior venda;
* Menor venda.

---

## Aprendizados Aplicados

Este projeto foi desenvolvido com foco em consolidar conhecimentos de:

* Python;
* Manipulação de arquivos;
* Expressões regulares;
* Pandas;
* Tratamento de dados;
* Construção de pipelines simples;
* Streamlit;
* Visualização de dados;
* Estruturação de projetos reais.

Além da solução prática para o negócio, o projeto também serve como laboratório de estudo para desenvolvimento de competências em:

* Análise de Dados;
* Engenharia de Dados;
* Automação de Processos;
* Desenvolvimento de Aplicações em Python.

---

## Próximas Evoluções

* Integração com PostgreSQL;
* Integração com Supabase;
* Automações utilizando n8n;
* Insights automáticos;
* Dashboard avançado;
* Upload automatizado de documentos;
* API para ingestão de dados;
* Processamento em lote agendado.

---

## Como Executar

### Clonar o repositório

```bash
git clone <url-do-repositorio>
```

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar ambiente virtual

Windows:

```bash
.venv\Scripts\activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar aplicação

```bash
streamlit run app.py
```

---

## Autor

Michael Lima

Projeto desenvolvido com foco em automação, análise de dados e construção de soluções para problemas reais de negócio utilizando Python.
