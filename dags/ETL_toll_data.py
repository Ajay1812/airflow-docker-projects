from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
import os
import logging
import pandas as pd

PATH="/opt/airflow/data/extracted_data/"

default_args = {
    'owner' : 'nf_01',
    "start_date" : datetime(2024, 2, 8),
    'retries' : 1
}

dag = DAG(
    dag_id="unzip_data",
    description="DAG for tollplaza data",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup = False
    )

download_data = BashOperator(
    task_id="download_tar",
    bash_command=f"""
    mkdir -p {PATH} && chmod -R 777 {PATH} && curl https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz -o {PATH}tolldata.tgz
    """,
    dag=dag
)
unzip_data = BashOperator(
    task_id="unzip_data_from_tar",
    bash_command = f"""
    tar -xvf {PATH}tolldata.tgz -C {PATH} && rm {PATH}fileformats.txt && rm -f {PATH}tolldata.tgz 
    """,
    dag=dag
)
extract_data_from_csv = BashOperator(
    task_id="extract_data_from_csv",
    bash_command=f"""
    cut -d ',' -f1,2,3,4 {PATH}vehicle-data.csv > {PATH}csv_data.csv 
    """,
    dag=dag
)
extract_data_from_tsv = BashOperator(
    task_id="extract_data_from_tsv",
    bash_command=f"""
    cut -f5,6,7 {PATH}tollplaza-data.tsv | cut -c1-14 | tr '\t' ',' > {PATH}tsv_data.csv 
    """,
    dag=dag
)
extract_data_from_fixed_width = BashOperator(
    task_id="extract_data_from_fixed_width",
    bash_command=f"""
    rev {PATH}payment-data.txt | cut -c1-9 | rev | tr ' ' ',' > {PATH}fixed_width_data.csv 
    """,
    dag=dag
)
consolidate_data = BashOperator(
    task_id="consolidate_data",
    bash_command=f"""
    paste -d',' {PATH}csv_data.csv {PATH}tsv_data.csv {PATH}fixed_width_data.csv > {PATH}extracted_data.csv
    """
)

transform_data = BashOperator(
    task_id="transform_data",
    bash_command=f"""
    cut -d',' -f4 {PATH}extracted_data.csv | tr '[:lower:]' '[:upper:]' > {PATH}vehicle_type.csv && paste -d',' <(cut -d',' -f1,2,3 {PATH}extracted_data.csv) {PATH}vehicle_type.csv <(cut -d',' -f5,6,7,8,9 {PATH}extracted_data.csv) > {PATH}transformed_data.csv
    """,
    dag=dag
)

cleanup = BashOperator(
    task_id="cleanup",
    bash_command=f"""
    cd {PATH} && rm csv_data.csv extracted_data.csv fixed_width_data.csv payment-data.txt tollplaza-data.tsv tsv_data.csv vehicle-data.csv vehicle_type.csv
    """,
    dag=dag
)

download_data >> unzip_data >> [extract_data_from_csv, extract_data_from_tsv, extract_data_from_fixed_width] >> consolidate_data >> transform_data >> cleanup