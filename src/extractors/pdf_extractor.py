
import pdfplumber
import re

# =======================================================================
# função para extrair texto bruto do PDF

def extract_text_from_pdf(pdf_file):
    """
    Extrai o texto bruto de um arquivo PDF.

    Parâmetros:
        pdf_file: arquivo PDF enviado pelo Streamlit.

    Retorno:
        texto_completo: texto extraído de todas as páginas do PDF.
    """

    texto_extraido = ""

    with pdfplumber.open(pdf_file) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()

            if texto_pagina:
                texto_extraido += texto_pagina + "\n"

    return texto_extraido


# =======================================================================

def extrair_dados_recibo(texto):
    """
    Extrai dados principais de um recibo a partir do texto bruto.
    """

    numero_recibo = re.search(r'Recibo nº:\s*(\d+)', texto)
    cliente = re.search(r'Cliente:\s*(.+)', texto)
    valor = re.search(r'Valor Total:\s*R\$\s*([\d.,]+)', texto)
    data = re.search(r'Data:\s*(.+)',texto)


    return {
        "numero_recibo": numero_recibo.group(1) if numero_recibo else None,
        "data": data.group(1) if data else None,
        "cliente": cliente.group(1) if cliente else None,
        "valor": valor.group(1) if valor else None
    }
