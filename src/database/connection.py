import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

load_dotenv()


def get_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    connection_string = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    return create_engine(connection_string)


def salvar_recibos_postgres(df):
    engine = get_engine()

    if df is None or df.empty:
        return 0

    df = df.copy()
    df = df.rename(columns={"dados": "data"})
    df = df[["numero_recibo", "data", "cliente", "valor", "arquivo_origem"]]
    df = df.drop_duplicates(subset=["numero_recibo"])

    query = text("""
        INSERT INTO recibos (
            numero_recibo,
            data,
            cliente,
            valor,
            arquivo_origem
        )
        VALUES (
            :numero_recibo,
            :data,
            :cliente,
            :valor,
            :arquivo_origem
        )
        ON CONFLICT (numero_recibo) DO NOTHING
    """)

    dados = df.to_dict(orient="records")

    with engine.begin() as conn:
        result = conn.execute(query, dados)

    return result.rowcount


# def salvar_recibos_postgres(df):
#     engine = get_engine()

#     recibos_existentes = pd.read_sql(
#         "SELECT numero_recibo FROM recibos",
#         con=engine
#     )

#     df_novos = df[
#         ~df["numero_recibo"].isin(recibos_existentes["numero_recibo"])
#     ]

#     if df_novos.empty:
#         return 0

#     df_novos.to_sql(
#         name="recibos",
#         con=engine,
#         if_exists="append",
#         index=False
#     )

#     return len(df_novos)

 

# from sqlalchemy import text


