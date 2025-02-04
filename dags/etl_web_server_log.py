from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import urllib.request
import pandas as pd
import logging


if not os.path.exists("./data"):
    os.makedirs("./data")

EXTRACTED_FILE = "./data/web-server-access-log.txt"
TRANSFORMED_FILE = "./data/transform_Data.csv"
OUTPUT_FILE = './data/capitalized.txt'

def extract():
    logging.info("Starting extract process...")
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode('utf-8')
    with open(EXTRACTED_FILE, 'w') as f:
        f.write(data)
    logging.info("Extract process completed.")

def transform():
    logging.info("Starting transform process...")
    df = pd.read_csv(filepath_or_buffer=EXTRACTED_FILE, delimiter='#')
    df['visitorid'] = df['visitorid'].str.upper()
    df.to_csv(TRANSFORMED_FILE, header=True, index=False)
    logging.info("Transform process completed.")

def load():
    logging.info("Starting load process...")
    df = pd.read_csv(TRANSFORMED_FILE)
    with open(OUTPUT_FILE, 'w') as f:
        for _, row in df.iterrows():
            write_Data = row['timestamp'] + "," + row['visitorid'] + "\n"
            f.write(write_Data)
    logging.info("Load process completed.")


# DAG Default Arguments
default_args = {
    'owner': 'nf_01',
    'start_date': datetime(2025, 2, 3),
    'retries': 0,
    'retry_delay': timedelta(minutes=50),
}

dag = DAG(
    dag_id='ETL_for_web_server_log',
    description='DAG for server log',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False
)

extract_data = PythonOperator(
    task_id='extract_data',
    python_callable=extract,
    dag=dag
)

transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform,
    dag=dag
)

load_data = PythonOperator(
    task_id='load_data',
    python_callable=load,  
    dag=dag
)

extract_data >> transform_data >> load_data
