from dateparser import parse
import pandas as pd


def transformar_dados(nome):
   
    relatorio = pd.DataFrame(nome) #transformando Json em DataFrame pra analise com Pandas

    relatorio['data'] = relatorio['data'].apply(parse) #convertendo data (1 de janeiro de 2026 > 01/01/2026)

    relatorio['data'] = pd.to_datetime(relatorio['data']) # convertendo data String > DateTime

    relatorio['valor'] = (
        relatorio['valor']
        .fillna('0')
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
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