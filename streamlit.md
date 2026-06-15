# Prompt para IA — Construção da Interface Streamlit do Projeto `document-intelligence`

## Contexto do projeto

Você é uma IA desenvolvedora Python/Streamlit. Sua tarefa é refatorar e melhorar a interface de uma aplicação existente que extrai dados de recibos em PDF.

O projeto atual já possui uma aplicação em Streamlit que permite o upload de múltiplos PDFs, extrai informações com `pdfplumber` e `regex`, transforma os dados em dicionários, converte para `DataFrame` com `pandas`, faz limpeza/conversão dos dados e permite exportar o resultado para CSV.

O objetivo agora é criar uma interface visual mais profissional, no estilo dashboard premium dark, semelhante ao modelo de referência enviado pelo usuário.

---

## Objetivo da entrega

Criar uma interface Streamlit com aparência moderna, escura, premium e organizada para o projeto de extração de dados de PDFs.

A interface deve conter:

1. Sidebar lateral com identidade do projeto e navegação.
2. Área principal com título e descrição.
3. Cards de indicadores principais.
4. Área de upload de PDFs.
5. Tabela com preview dos dados extraídos.
6. Gráficos simples baseados no DataFrame extraído.
7. Botão para exportar CSV.
8. Área futura para conexão com Power BI.
9. Estilo visual usando CSS customizado no próprio Streamlit.

---

## Nome genérico do projeto

Use o nome:

```text
document-intelligence
```

Título visual na aplicação:

```text
Document Intelligence
PDF Data Pipeline
```

Evite qualquer referência ao nome real da empresa/oficina.

---

## Paleta de cores obrigatória

Use uma estética `Premium Dark` com preto, grafite e dourado.

```text
Fundo Principal: #050505
Fundo Secundário: #0D0D0D
Cards: #121212
Bordas: #4A3B26
Dourado Principal: #C6A36A
Dourado Claro: #D9BC8A
Dourado Escuro: #8A6B42
Texto Principal: #F5F5F5
Texto Secundário: #B0B0B0
Texto Terciário: #7A7A7A
Sucesso: #22C55E
Erro: #EF4444
Alerta: #F59E0B
```

O visual deve parecer um dashboard executivo escuro com detalhes em dourado.

---

## Dependências já usadas no projeto

Considere que o projeto utiliza ou poderá utilizar:

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from dateparser import parse

from src.extractors.pdf_extractor import extract_text_from_pdf, extrair_dados_recibo
from src.transformers.pedido_transformer import transformar_dados
```

Não remova a lógica existente de extração. Apenas melhore a interface e organize melhor a experiência do usuário.

---

## Estrutura esperada do DataFrame extraído

Considere que o CSV/DataFrame extraído dos PDFs pode conter colunas semelhantes a estas:

```text
numero_recibo
cliente
valor_final
data_recibo
arquivo_origem
```

Também podem existir variações como:

```text
recibo
nome_cliente
valor
data
arquivo
```

A interface deve ser tolerante. Antes de calcular métricas, valide se as colunas existem.

---

## Indicadores principais

Criar cards no topo da página principal com:

### 1. PDFs Processados
Quantidade de arquivos PDF enviados ou quantidade de linhas extraídas.

### 2. Valor Total
Soma da coluna de valor, quando existir.

### 3. Registros Extraídos
Quantidade de registros no DataFrame.

### 4. Clientes Únicos
Quantidade de clientes únicos, quando existir coluna de cliente.

Exemplo visual:

```text
┌────────────────────┐
│ Valor Total        │
│ R$ 12.450,00       │
│ Dados extraídos    │
└────────────────────┘
```

---

## Layout desejado

Criar uma interface semelhante a este conceito:

```text
┌───────────────────────────────────────────────────────────────┐
│ Sidebar                 │ Header + KPIs                       │
│                         │ Upload PDFs + Tabela recentes       │
│ - Dashboard             │ Gráfico faturamento por dia          │
│ - Extrair PDF           │ Gráfico valor por cliente            │
│ - Dados Extraídos       │ Exportar CSV                         │
│ - Configurações         │ Link futuro Power BI                 │
└───────────────────────────────────────────────────────────────┘
```

---

## Sidebar

A sidebar deve conter:

```text
Document Intelligence
PDF Data Pipeline

Dashboard
Extrair PDF
Dados Extraídos
Configurações
Sobre

Banco de Dados
Status: Local / Futuro PostgreSQL
Versão: 1.0.0
```

Use ícones com emojis ou texto simples. Não adicione dependências externas apenas para ícones.

---

## Upload de PDFs

Criar uma área visual destacada para upload:

```text
Extrair Novos PDFs
Arraste e solte seus arquivos PDF aqui
ou clique para selecionar
Suporta múltiplos arquivos
```

Use:

```python
st.file_uploader(
    "",
    type=["pdf"],
    accept_multiple_files=True,
    key="upload_pdfs"
)
```

Após processar, mostrar:

```text
PDFs processados com sucesso
CSV pronto para exportação
```

Se houver erro, mostrar mensagem amigável.

---

## Preview dos dados extraídos

Após extração, mostrar uma tabela com os dados:

```python
st.dataframe(df, use_container_width=True)
```

Antes da tabela, mostrar:

```text
Dados Extraídos
Visualização dos registros processados a partir dos PDFs enviados.
```

---

## Gráficos

Criar gráficos apenas se as colunas necessárias existirem.

### Gráfico 1 — Valor por cliente

Se existir coluna de cliente e valor:

```python
df_cliente = df.groupby(col_cliente)[col_valor].sum().reset_index()
fig = px.bar(df_cliente, x=col_valor, y=col_cliente, orientation="h")
st.plotly_chart(fig, use_container_width=True)
```

### Gráfico 2 — Valor por data

Se existir coluna de data e valor:

```python
df_data = df.groupby(col_data)[col_valor].sum().reset_index()
fig = px.line(df_data, x=col_data, y=col_valor, markers=True)
st.plotly_chart(fig, use_container_width=True)
```

### Gráfico 3 — Distribuição por cliente

Se existir cliente e valor:

```python
fig = px.pie(df_cliente, values=col_valor, names=col_cliente, hole=0.55)
st.plotly_chart(fig, use_container_width=True)
```

Aplicar tema escuro e cores douradas nos gráficos.

---

## Exportação CSV

Manter botão de download:

```python
csv = df.to_csv(index=False, sep=";", encoding="utf-8-sig")

st.download_button(
    label="Baixar CSV",
    data=csv,
    file_name="dados_extraidos.csv",
    mime="text/csv"
)
```

---

## CSS customizado obrigatório

Adicionar CSS dentro do Streamlit usando:

```python
st.markdown("""
<style>
...
</style>
""", unsafe_allow_html=True)
```

O CSS deve alterar:

- Fundo da aplicação.
- Fundo dos cards.
- Bordas arredondadas.
- Bordas douradas discretas.
- Botões com gradiente dourado.
- Textos em branco/cinza.
- Sidebar escura.

Estilo esperado:

```css
.main {
    background-color: #050505;
}

.metric-card {
    background: linear-gradient(145deg, #121212, #0D0D0D);
    border: 1px solid #4A3B26;
    border-radius: 16px;
    padding: 20px;
}
```

---

## Função auxiliar para cards

Criar uma função semelhante:

```python
def render_metric_card(title, value, subtitle=""):
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-title">{title}</p>
        <h2 class="metric-value">{value}</h2>
        <p class="metric-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
```

---

## Regras importantes

1. Não quebrar a lógica atual do projeto.
2. Não adicionar dependências desnecessárias.
3. Não criar conexão com PostgreSQL ainda.
4. Não criar Docker ainda.
5. O foco desta etapa é somente finalizar a interface Streamlit.
6. O código deve ser limpo, legível e organizado.
7. Validar colunas antes de criar métricas e gráficos.
8. Usar `st.session_state` se necessário para manter o DataFrame após o upload.
9. Usar nomes genéricos, sem mencionar empresa real.

---

## Resultado esperado

Ao final, a aplicação deve permitir que o usuário:

1. Acesse uma interface visual profissional.
2. Envie vários PDFs.
3. Visualize os dados extraídos.
4. Veja indicadores principais.
5. Veja gráficos simples.
6. Baixe o CSV tratado.

A tela deve transmitir a ideia de uma plataforma de dados, não apenas um script de upload.

---

## Próximas fases do projeto

Não implementar agora, apenas deixar a estrutura preparada para evoluir depois:

```text
Fase 1 — Interface Streamlit
Fase 2 — PostgreSQL local
Fase 3 — Power BI conectado ao banco
Fase 4 — Dashboard final no Power BI
Fase 5 — Docker
```

