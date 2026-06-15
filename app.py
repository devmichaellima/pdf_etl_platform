# =======================================================================
# Bibliotecas
import os
import pandas as pd
import plotly.express as px
import streamlit as st
from dateparser import parse

from src.extractors.pdf_extractor import extract_text_from_pdf, extrair_dados_recibo
from src.transformers.pedido_transformer import transformar_dados

# =======================================================================
# Configurações da página
st.set_page_config(
    page_title='Document Intelligence - Dashboard', 
    page_icon='📄',
    layout='wide',
    initial_sidebar_state='expanded'
)

# =======================================================================
# Injeção de CSS Customizado (Premium Dark Theme)
st.markdown("""
<style>
/* Ocultar cabeçalho padrão e rodapé do Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Tipografia e cores básicas do corpo */
body {
    background-color: #050505;
    color: #F5F5F5;
    font-family: 'Inter', sans-serif;
}

/* Customização da Barra Lateral (Sidebar) */
section[data-testid="stSidebar"] {
    background-color: #0D0D0D !important;
    border-right: 1px solid #4A3B26;
    padding-top: 20px;
}

section[data-testid="stSidebar"] .stMarkdown {
    color: #F5F5F5;
}

/* Customização dos botões de rádio na navegação */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: #121212;
    border: 1px solid #2A2218;
    border-radius: 8px;
    padding: 10px 15px;
    margin-bottom: 8px;
    color: #B0B0B0 !important;
    transition: all 0.3s ease;
    cursor: pointer;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    border-color: #C6A36A;
    color: #F5F5F5 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"] {
    background: linear-gradient(135deg, #121212 0%, #2A2218 100%) !important;
    border-color: #C6A36A !important;
    color: #C6A36A !important;
    font-weight: bold;
}

/* Cards de Métricas Personalizados */
.metric-card {
    background: linear-gradient(135deg, #121212 0%, #0D0D0D 100%);
    border: 1px solid #4A3B26;
    border-radius: 12px;
    padding: 22px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    margin-bottom: 15px;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #C6A36A, #8A6B42);
}

.metric-card {
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

# .metric-card:hover {
#     transform: translateY(-4px);
#     border-color: #C6A36A;
#     box-shadow: 0 8px 30px rgba(198, 163, 106, 0.15);
# }

.metric-title {
    color: #B0B0B0;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 0 0 8px 0;
}

.metric-value {
    color: #C6A36A;
    font-size: clamp(24px, 2.2vw, 34px);
    font-weight: 700;
    margin: 0 0 4px 0;
    font-family: 'Outfit', sans-serif;
    white-space: nowrap;
}

# .metric-value {
#     color: #C6A36A;
#     font-size: 28px;
#     font-weight: 700;
#     margin: 0 0 4px 0;
#     font-family: 'Outfit', sans-serif;
# }

.metric-subtitle {
    color: #7A7A7A;
    font-size: 11px;
    margin: 0;
}

/* Customização Geral de Botões */
div.stButton > button {
    background: linear-gradient(90deg, #8A6B42 0%, #C6A36A 100%) !important;
    color: #050505 !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 6px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 15px rgba(198, 163, 106, 0.15) !important;
    transition: all 0.3s ease !important;
    width: 100%;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #C6A36A 0%, #D9BC8A 100%) !important;
    color: #050505 !important;
    box-shadow: 0 6px 20px rgba(198, 163, 106, 0.3) !important;
    transform: translateY(-2px);
}

div.stDownloadButton > button {
    background: linear-gradient(90deg, #8A6B42 0%, #C6A36A 100%) !important;
    color: #050505 !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 6px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 15px rgba(198, 163, 106, 0.15) !important;
    transition: all 0.3s ease !important;
}

div.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #C6A36A 0%, #D9BC8A 100%) !important;
    color: #050505 !important;
    box-shadow: 0 6px 20px rgba(198, 163, 106, 0.3) !important;
    transform: translateY(-2px);
}

/* Customização do File Uploader */
section[data-testid="stFileUploader"] {
    background-color: #0D0D0D;
    border: 1px dashed #4A3B26;
    border-radius: 12px;
    padding: 20px;
    transition: border-color 0.3s ease;
}

section[data-testid="stFileUploader"]:hover {
    border-color: #C6A36A;
}

/* Info e Info Cards */
.info-card {
    background-color: #0D0D0D;
    border: 1px solid #4A3B26;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}

/* Customização de scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #050505;
}
::-webkit-scrollbar-thumb {
    background: #4A3B26;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #C6A36A;
}
</style>
""", unsafe_allow_html=True)

# =======================================================================
# Inicialização do Session State
if 'df_dados' not in st.session_state:
    st.session_state['df_dados'] = None

if 'total_files' not in st.session_state:
    st.session_state['total_files'] = 0

# Tenta carregar dados pré-existentes na inicialização
csv_path = 'data/relatorio.csv'
if st.session_state['df_dados'] is None and os.path.exists(csv_path):
    try:
        df_init = pd.read_csv(csv_path)
        if 'data' in df_init.columns:
            # Garante que a data seja parseada como datetime
            df_init['data'] = pd.to_datetime(df_init['data'], format='%d/%m/%Y', errors='coerce')
        st.session_state['df_dados'] = df_init
        
        # Como carregamos dados já prontos, consideramos os registros como ponto de partida
        st.session_state['total_files'] = df_init['arquivo_origem'].nunique() if 'arquivo_origem' in df_init.columns else len(df_init)
    except Exception:
        pass

# =======================================================================
# Sidebar (Painel de Identidade e Navegação)
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <h2 style="color: #C6A36A; margin-bottom: 2px; font-weight: 700; font-family: 'Outfit', sans-serif; letter-spacing: 0.5px;">Document Intelligence</h2>
        <p style="color: #7A7A7A; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin: 0;">PDF Data Pipeline</p>
    </div>
    <hr style="border-color: #4A3B26; margin-top: 0; margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    # Navegação por botões de rádio (customizados via CSS)
    opcao_menu = st.radio(
        label="Navegação",
        options=["Dashboard", "Extrair PDF", "Dados Extraídos", "Configurações", "Sobre"],
        label_visibility="collapsed"
    )
    
    # Rodapé fixo na sidebar com status
    st.markdown("""
    <div style="margin-top: 60px; padding: 15px; border-top: 1px solid #4A3B26;">
        <p style="margin: 0; font-size: 10px; color: #7A7A7A; text-transform: uppercase; letter-spacing: 1px;">Banco de Dados</p>
        <p style="margin: 2px 0 10px 0; font-size: 13px; color: #B0B0B0; font-weight: 600;">Status: <span style="color: #C6A36A;">Local / CSV</span></p>
        <p style="margin: 0; font-size: 10px; color: #7A7A7A; text-transform: uppercase; letter-spacing: 1px;">Versão: <span style="color: #B0B0B0;">1.0.0</span></p>
    </div>
    """, unsafe_allow_html=True)

# =======================================================================
# Funções de renderização de componentes
def render_metric_card(title, value, subtitle=""):
    return f"""
    <div class="metric-card">
        <p class="metric-title">{title}</p>
        <h2 class="metric-value">{value}</h2>
        <p class="metric-subtitle">{subtitle}</p>
    </div>
    """

def show_kpis(df, total_files):
    pdf_count = total_files
    records_count = len(df) if df is not None else 0
    
    # Validações antes de calcular
    if df is not None and not df.empty and 'valor' in df.columns:
        total_val = df['valor'].sum()
        total_val_str = f"R$ {total_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        total_val_str = "R$ 0,00"
        
    if df is not None and not df.empty and 'cliente' in df.columns:
        unique_clients = df['cliente'].nunique()
    else:
        unique_clients = 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_metric_card("PDFs Processados", f"{pdf_count}", "Arquivos lidos e validados"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card("Valor Total", total_val_str, "Soma consolidada dos valores"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card("Registros Extraídos", f"{records_count}", "Total de linhas na base"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_metric_card("Clientes Únicos", f"{unique_clients}", "Clientes distintos identificados"), unsafe_allow_html=True)

# =======================================================================
# Abas / Telas da aplicação

# -----------------------------------------------------------------------
# TELA: Dashboard
if "Dashboard" in opcao_menu:
    st.markdown("<h1 style='color: #F5F5F5; font-family: Outfit, sans-serif;'>Painel de Indicadores</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #B0B0B0;'>Acompanhe o faturamento, registros extraídos e performance dos clientes.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    df = st.session_state['df_dados']
    
    # KPIs principais
    show_kpis(df, st.session_state['total_files'])
    st.markdown("<br>", unsafe_allow_html=True)
    
    if df is not None and not df.empty:
        # Layout de Gráficos (Data e Distribuição de clientes lado a lado)
        col_g1, col_g2 = st.columns([2, 1])
        
        with col_g1:
            if 'data' in df.columns and 'valor' in df.columns:
                # Tratar datas nulas antes de agrupar
                df_clean_data = df.dropna(subset=['data', 'valor'])
                df_data = df_clean_data.groupby('data')['valor'].sum().reset_index()
                df_data = df_data.sort_values('data')
                
                fig_line = px.line(
                    df_data,
                    x='data',
                    y='valor',
                    title="Evolução de Faturamento por Data",
                    markers=True,
                    color_discrete_sequence=["#C6A36A"]
                )
                fig_line.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#121212",
                    plot_bgcolor="#121212",
                    xaxis=dict(
                        title="Data do Recibo",
                        gridcolor="#2A2218",
                        linecolor="#4A3B26"
                    ),
                    yaxis=dict(
                        title="Faturamento (R$)",
                        gridcolor="#2A2218",
                        linecolor="#4A3B26"
                    ),
                    font=dict(color="#F5F5F5", family="Inter, sans-serif"),
                    title_font=dict(color="#C6A36A", size=16, family="Outfit, sans-serif")
                )
                fig_line.update_traces(line=dict(width=3), marker=dict(size=8, color="#D9BC8A"))
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("Colunas necessárias para o gráfico de faturamento por data não estão presentes.")
                
        with col_g2:
            if 'cliente' in df.columns and 'valor' in df.columns:
                df_clean_cli = df.dropna(subset=['cliente', 'valor'])
                df_cli_dist = df_clean_cli.groupby('cliente')['valor'].sum().reset_index()
                df_cli_dist = df_cli_dist.sort_values('valor', ascending=False).head(5)
                
                fig_pie = px.pie(
                    df_cli_dist,
                    values='valor',
                    names='cliente',
                    hole=0.55,
                    title="Distribuição (Top 5 Clientes)",
                    color_discrete_sequence=["#C6A36A", "#D9BC8A", "#8A6B42", "#E5C494", "#B38F56"]
                )
                fig_pie.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#121212",
                    font=dict(color="#F5F5F5", family="Inter, sans-serif"),
                    title_font=dict(color="#C6A36A", size=16, family="Outfit, sans-serif"),
                    legend=dict(font=dict(size=10), orientation="h", y=-0.1)
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Colunas necessárias para o gráfico de distribuição de clientes não estão presentes.")
                
        # Gráfico horizontal - Clientes
        st.markdown("<br>", unsafe_allow_html=True)
        if 'cliente' in df.columns and 'valor' in df.columns:
            df_clean_cli = df.dropna(subset=['cliente', 'valor'])
            df_cli_bar = df_clean_cli.groupby('cliente')['valor'].sum().reset_index()
            df_cli_bar = df_cli_bar.sort_values('valor', ascending=True).tail(10)
            
            fig_bar = px.bar(
                df_cli_bar,
                x='valor',
                y='cliente',
                orientation='h',
                title="Top 10 Clientes por Volume Financeiro",
                color_discrete_sequence=["#C6A36A"]
            )
            fig_bar.update_layout(
                template="plotly_dark",
                paper_bgcolor="#121212",
                plot_bgcolor="#121212",
                xaxis=dict(
                    title="Faturamento Acumulado (R$)",
                    gridcolor="#2A2218",
                    linecolor="#4A3B26"
                ),
                yaxis=dict(
                    title="Cliente",
                    gridcolor="#2A2218",
                    linecolor="#4A3B26"
                ),
                font=dict(color="#F5F5F5", family="Inter, sans-serif"),
                title_font=dict(color="#C6A36A", size=16, family="Outfit, sans-serif")
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
    else:
        st.markdown("""
        <div class="info-card" style="text-align: center; padding: 40px 20px;">
            <h3 style="color: #C6A36A; margin-bottom: 10px;">Nenhum dado processado</h3>
            <p style="color: #B0B0B0; max-width: 500px; margin: 0 auto 20px auto;">
                Ainda não há recibos processados no pipeline. Para carregar e extrair dados dos arquivos PDF, navegue até a aba lateral <b>Extrair PDF</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------
# TELA: Extrair PDF
elif "Extrair PDF" in opcao_menu:
    st.markdown("<h1 style='color: #F5F5F5; font-family: Outfit, sans-serif;'>Extrair Novos PDFs</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #B0B0B0;'>Carregue múltiplos arquivos de recibo em formato PDF para rodar o pipeline de inteligência documental.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Controle de Uploader
    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = 0
        
    st.markdown("<h4 style='color: #C6A36A;'>Selecione os arquivos PDF</h4>", unsafe_allow_html=True)
    
    arquivos_pdf = st.file_uploader(
        label="Clique para carregar ou arraste e solte os arquivos aqui.",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"upload_pdfs_{st.session_state['uploader_key']}",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        btn_processar = st.button("Processar Arquivos")
    with col_btn2:
        btn_limpar = st.button("Limpar lista de upload")
        
    if btn_limpar:
        st.session_state["uploader_key"] += 1
        st.rerun()
        
    if btn_processar:
        if not arquivos_pdf:
            st.warning("⚠️ Selecione ao menos um arquivo PDF antes de executar o processamento.")
        else:
            base_dados = []
            process_bar = st.progress(0)
            status_text = st.empty()
            
            for index, arquivo in enumerate(arquivos_pdf):
                status_text.markdown(f"<span style='color: #B0B0B0;'>Extraindo dados de: <b>{arquivo.name}</b>...</span>", unsafe_allow_html=True)
                try:
                    texto_extraido = extract_text_from_pdf(arquivo)
                    dados_coletados = extrair_dados_recibo(texto_extraido)
                    
                    # Armazena o arquivo de origem
                    dados_coletados["arquivo_origem"] = arquivo.name
                    
                    base_dados.append(dados_coletados)
                except Exception as e:
                    st.error(f"❌ Erro ao extrair texto de {arquivo.name}: {str(e)}")
                
                # Atualiza barra de progresso
                process_bar.progress((index + 1) / len(arquivos_pdf))
                
            status_text.empty()
            
            if base_dados:
                with st.spinner("Transformando e consolidando dados..."):
                    try:
                        relatorio = transformar_dados(base_dados)
                        
                        # Cria pasta 'data' caso não exista
                        os.makedirs('data', exist_ok=True)
                        
                        # Exporta CSV local (separador default ',' para o sistema interno)
                        relatorio.to_csv(
                            'data/relatorio.csv', 
                            index=False,
                            date_format='%d/%m/%Y'
                        )
                        
                        # Salva no session state
                        st.session_state['df_dados'] = relatorio
                        st.session_state['total_files'] = len(arquivos_pdf)
                        
                        st.markdown(f"""
                        <div style='background-color: #121212; border: 1px solid #22C55E; padding: 15px; border-radius: 8px; margin-top: 15px;'>
                            <h4 style='color: #22C55E; margin: 0 0 5px 0;'>✓ PDFs processados com sucesso!</h4>
                            <p style='color: #B0B0B0; margin: 0; font-size: 13px;'>Consolidado {len(relatorio)} registros. O arquivo CSV já está pronto para exportação.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao formatar dados extraídos: {str(e)}")
            else:
                st.error("❌ Nenhum dado válido foi extraído dos PDFs informados.")

# -----------------------------------------------------------------------
# TELA: Dados Extraídos
elif "Dados Extraídos" in opcao_menu:
    st.markdown("<h1 style='color: #F5F5F5; font-family: Outfit, sans-serif;'>Dados Extraídos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #B0B0B0;'>Visualização e download dos registros processados a partir dos PDFs enviados.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    df = st.session_state['df_dados']
    
    if df is not None and not df.empty:
        # Prepara o download do CSV formatado com ';' para Excel compatibilidade
        # Formata o DataFrame antes de gerar o CSV para salvar as datas no formato brasileiro dd/mm/yyyy
        df_export = df.copy()
        if 'data' in df_export.columns:
            df_export['data'] = df_export['data'].dt.strftime('%d/%m/%Y')
            
        csv_data = df_export.to_csv(index=False, sep=";", encoding="utf-8-sig")
        
        col_spaced, col_btn_download = st.columns([3, 1])
        with col_btn_download:
            st.download_button(
                label="Baixar CSV (Sep:';')",
                data=csv_data,
                file_name="dados_extraidos.csv",
                mime="text/csv"
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        
    else:
        st.markdown("""
        <div class="info-card" style="text-align: center; padding: 40px 20px;">
            <h3 style="color: #C6A36A; margin-bottom: 10px;">Sem dados disponíveis</h3>
            <p style="color: #B0B0B0; max-width: 500px; margin: 0 auto;">
                Faça o upload dos recibos na aba <b>Extrair PDF</b> para visualizar a tabela detalhada nesta seção.
            </p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------
# TELA: Configurações
elif "Configurações" in opcao_menu:
    st.markdown("<h1 style='color: #F5F5F5; font-family: Outfit, sans-serif;'>Configurações do Pipeline</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #B0B0B0;'>Ajuste as definições do pipeline de dados, conexões de banco de dados e integrações.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4 style="color: #C6A36A; margin-bottom: 15px;">Integração com Banco de Dados (Preparada para Fase 2)</h4>
    """, unsafe_allow_html=True)
    
    db_mode = st.selectbox(
        "Armazenamento de Destino",
        ["Local (Arquivos CSV)", "PostgreSQL (Futuro - Conexão Direta)"]
    )
    
    col_db1, col_db2 = st.columns(2)
    with col_db1:
        st.text_input("Host do Banco de Dados", value="localhost", disabled=(db_mode == "Local (Arquivos CSV)"))
        st.text_input("Porta", value="5432", disabled=(db_mode == "Local (Arquivos CSV)"))
        st.text_input("Nome do Banco (Database)", value="document_intelligence", disabled=(db_mode == "Local (Arquivos CSV)"))
    with col_db2:
        st.text_input("Usuário", value="postgres", disabled=(db_mode == "Local (Arquivos CSV)"))
        st.text_input("Senha", value="*****", type="password", disabled=(db_mode == "Local (Arquivos CSV)"))
        st.text_input("Esquema (Schema)", value="public", disabled=(db_mode == "Local (Arquivos CSV)"))
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4 style="color: #C6A36A; margin-bottom: 15px;">Parâmetros Globais do Pipeline</h4>
    """, unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.checkbox("Sobrescrever CSV anterior a cada extração", value=True)
        st.checkbox("Limpar espaços extras dos nomes de clientes", value=True)
    with col_p2:
        st.checkbox("Validar integridade de valores monetários", value=True)
        st.checkbox("Armazenar histórico dos arquivos físicos (Backup)", value=False)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Salvar Configurações"):
        st.success("Configurações salvas localmente (Modo Mock ativo)!")

# -----------------------------------------------------------------------
# TELA: Sobre
elif "Sobre" in opcao_menu:
    st.markdown("<h1 style='color: #F5F5F5; font-family: Outfit, sans-serif;'>Sobre o Document Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #B0B0B0;'>Estrutura e progresso evolutivo da plataforma.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4 style="color: #C6A36A; margin-bottom: 10px;">O Projeto</h4>
        <p style="color: #B0B0B0; line-height: 1.6;">
            O <b>Document Intelligence - PDF Data Pipeline</b> é uma ferramenta desenvolvida para resolver
            a ingestão e processamento automático de dados de recibos de vendas e ordens de serviços gerados em PDF.
            Através de técnicas eficientes de OCR/Leitura com <i>pdfplumber</i> e filtros em <i>Regex</i>, a ferramenta 
            elimina o preenchimento manual, reduzindo a zero os erros de digitação e poupando tempo na conciliação.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4 style="color: #C6A36A; margin-bottom: 15px;">Fases Evolutivas da Plataforma</h4>
        <div style="margin-left: 10px;">
            <p style="color: #22C55E; margin: 4px 0;"><b>✓ Fase 1: Interface Streamlit</b> — Visual Premium Dark, métricas executivas e exportação de relatórios rápidos (ATUAL).</p>
            <p style="color: #B0B0B0; margin: 4px 0;"><b>⚙ Fase 2: PostgreSQL Local</b> — Persistência real em banco relacional para manter histórico robusto.</p>
            <p style="color: #B0B0B0; margin: 4px 0;"><b>⚙ Fase 3: Conexão de Dados</b> — Criação de views e conectores específicos para ferramentas de Business Intelligence.</p>
            <p style="color: #B0B0B0; margin: 4px 0;"><b>⚙ Fase 4: Dashboards Avançados</b> — Criação de layouts interativos e consolidados no Power BI.</p>
            <p style="color: #B0B0B0; margin: 4px 0;"><b>⚙ Fase 5: Docker</b> — Containerização completa da interface e do banco de dados PostgreSQL para implantação com 1-clique.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)