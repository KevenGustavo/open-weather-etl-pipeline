from sqlalchemy import create_engine, text
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
port = os.getenv("POSTGRES_PORT")
host = "postgres"

def get_engine():
    logging.info(f"Conectando em {host}:{port}/{database}")
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

engine = get_engine()

def load_weather_data(table_name:str, df:pd.DataFrame):
    logging.info(f"Carregando os dados para tabela: {table_name}")
    df.to_sql(name=table_name, con=engine, if_exists="append", index=False)

    logging.info("Dados carregados com sucesso!")

    df_validation = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)
    logging.info(f"Total de {len(df_validation)} na tabela {table_name}!")