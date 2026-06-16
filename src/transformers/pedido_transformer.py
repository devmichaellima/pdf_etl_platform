from dateparser import parse
import pandas as pd
import re


# erros de digitação encontrado manualmente
correcoes = {
    "Aiton": "Ailton",
    "Antonio": "Antônio",
    "Edson": "Edinho",
    "Montana": "Edinho",
    "Pricila": "Priscila",
    "Pai": "Isabela"
}


def limpar_nome(nome):

    if pd.isna(nome):
        return None

    nome = str(nome).strip()

    # remove pontuação final
    nome = nome.replace(".", "")

    # pega apenas a primeira palavra
    primeiro_nome = nome.split()[0]

    # padroniza capitalização
    primeiro_nome = primeiro_nome.title()

    # aplica correções
    primeiro_nome = correcoes.get(
        primeiro_nome,
        primeiro_nome
    )

    return primeiro_nome


def transformar_dados(nome):
   
    relatorio = pd.DataFrame(nome) #transformando Json em DataFrame pra analise com Pandas

    relatorio['data'] = relatorio['data'].apply(parse) #convertendo data (1 de janeiro de 2026 > 01/01/2026)

    relatorio["cliente"] = relatorio["cliente"].apply(limpar_nome) #correcao de erros de ortografia e registro

    relatorio['data'] = pd.to_datetime(relatorio['data']) # convertendo data String > DateTime

    relatorio['valor'] = (
        relatorio['valor']
        .fillna('0')
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False) # regex ident. alguns caract como comandos, por isso desativamos
        .astype(float)
    ) # converte numero string 1.000,00 para float 1000.00

    relatorio['cliente'] = (
        relatorio['cliente']
        .fillna("Cliente não identificado")
        .str.strip()
        .str.lower()
        .str.title()
    ) # formatação dos nomes

    return relatorio


