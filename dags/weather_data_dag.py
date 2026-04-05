from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys, os

sys.path.insert(0, "/opt/airflow/src")

from extract_data import extract_weather_data 
from load_data import load_weather_data
from transform_data import transform_weather_data
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

API_KEY = os.getenv("API_KEY")
url = f'https://api.openweathermap.org/data/2.5/weather?q=São Luís,MA,BR&units=metric&appid={API_KEY}'

@dag(
    dag_id='open_weather_pipeline',
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5)
    },
    description="Weather Pipeline - Clima São Luís, MA",
    schedule="0 * * * *",
    start_date=datetime(2026,4,5),
    catchup=False,
    tags=["Weather","ETL"]
)

def open_weather_pipeline():

    @task
    def extract():
        extract_weather_data(url)
    
    @task
    def transform():
        df = transform_weather_data()
        df.to_parquet("/opt/airflow/data/temp_data.parquet", index=False)

    @task
    def load():
        import pandas as pd
        df = pd.read_parquet("/opt/airflow/data/temp_data.parquet")
        load_weather_data("slz_weather",df)

    extract() >> transform() >> load()

open_weather_pipeline()