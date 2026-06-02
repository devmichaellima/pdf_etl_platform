# =======================================================================
# Bibliotecas
import plotly.express as px
import streamlit as st
from dateparser import parse
import pandas as pd
from src.extractors.pdf_extractor import extract_text_from_pdf, extrair_dados_recibo
from src.transformers.pedido_transformer import transformar_dados


# =======================================================================
# Configurações da pagina


st.set_page_config(
    page_title='Tekar Dashboard', #titulo na aba do navegador 
    page_icon='📄',
    layout='wide'
)

st.title('Tekar - Dashboard') #title cria uma fonte maior
st.write(
    "Ferramenta para extrair dados de pedidos em PDF, "
    "gerar CSV e visualizar indicadores."
)


# =======================================================================
# Upload dos arquivos PDF

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0


arquivos_pdf = st.file_uploader(
    label="",
    type=["pdf"],
    accept_multiple_files=True,
    key=f"upload_pdfs_{st.session_state['uploader_key']}"
) # cria lista de PDFs


if st.button("Limpar arquivos enviados"):
    st.session_state["uploader_key"] += 1
    st.rerun() # limpa a lista gerando uma nova key


base_dados = [] #formara uma lista com um dicionario pra cada pdf

if arquivos_pdf:
    
    st.success(f"{len(arquivos_pdf)} arquivo(s) enviado(s) com sucesso.") #confirmação e quant. de arquiv.

    for arquivo in arquivos_pdf: #arquivo é um objeto e possui atributos consultaveis (ex. arquivo.name)
        
        texto_extraido = extract_text_from_pdf(arquivo) #extrai o texto do PDF
        
        dados_coletados = extrair_dados_recibo(texto_extraido) #coleta os dados do texto extraido e cria dicio.
        
        base_dados.append(dados_coletados) #adiciona dicionario na lista base_dados
        

else:
    st.info("Envie um ou mais arquivos PDF para começar.")

# agora temos os dados armazenador em 'base_dados'


# =======================================================================
# Criando csv para analise com os dados coletados dos PDF
# Transformacao dos dados

if base_dados:
    
    
    relatorio = transformar_dados(base_dados) # funcao criada pra padronizar os tipos e formas dos dados

    relatorio.to_csv(
        'data/relatorio.csv', 
        index=False,
        date_format='%d/%m/%Y' #formatacao pra nao aparecer 00:00:00 no csv
    ) # exporta o csv limpo e formatado pronto para analise na pasta data

    csv = relatorio.to_csv(
        index=False,
        date_format='%d/%m/%Y',
        sep=';'
    ) # armazena o relatorio na variavel csv

    st.download_button(
        label="Baixar Relatório",
        data=csv,
        file_name="relatorio_tekar.csv",
        mime="text/csv"
    ) # baixa o relatorio armazenado em formato csv

   
    # =======================================================================
    # gerando analises 

    st.subheader("Análise dos Dados:")

    total_recibos = len(relatorio)

    faturamento_total = relatorio["valor"].sum()

    ticket_medio = relatorio["valor"].mean()

    maior_venda = relatorio["valor"].max()

    melhor_cliente = relatorio.groupby('cliente')['valor'].sum().idxmax()
    # Armazenando os KPIs nas variaveis 

    col1, col2, col3, col4, col5= st.columns(5) # cria x blocos de texto lado a lado

    col1.metric(
        label="Total de recibos",
        value=total_recibos
    )

    col2.metric(
        label="Faturamento total",
        value=f"R$ {faturamento_total:,.2f}"
    )

    col3.metric(
        label="Ticket médio",
        value=f"R$ {ticket_medio:,.2f}"
    )

    col4.metric(
        label="Maior venda",
        value=f"R$ {maior_venda:,.2f}"
    )

    col5.metric(
        label='Melhor cliente',
        value=melhor_cliente
    )

 
    st.dataframe(relatorio, use_container_width=True) # mostra o df em forma de tabela


    # =======================================================================
    # Gráfico de faturamento por data

    st.subheader("Gráficos comparativos:")

    faturamento_por_data = (
        relatorio
        .groupby("data")["valor"]
        .sum()
        .reset_index() # dataframe(col..) > series (indice, valor), reset_index trata como (col1, col2)
    )

    grafico_faturamento = px.bar(
        faturamento_por_data,
        x="data",
        y="valor", # x e y sao os nomes das colunas do df 
        title="Faturamento por data",
        labels={
            "data": "Data",
            "valor": "Faturamento"
        }
    ) # armazenamos o grafico dentro da variavel pra expor com streamlit

    st.plotly_chart(
        grafico_faturamento,
        use_container_width=True
    ) # grafico na tela 