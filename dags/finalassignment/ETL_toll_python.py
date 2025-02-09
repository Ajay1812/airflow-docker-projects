from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import os
import pandas as pd
import requests
import tarfile
import glob
import re

os.makedirs("./data/extracted_toll_data", exist_ok=True)
PATH = "/opt/airflow/data/extracted_toll_data"

def download_dataset()->None:
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz"
    response = requests.get(url, stream = True)
    with open(f"{PATH}/tolldata.tgz","wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def untar_dataset()->None:
    with tarfile.open(f"{PATH}/tolldata.tgz", "r:gz") as f:
        f.extractall(PATH)
    for file in glob.glob(f"{PATH}/._*"):
        os.remove(file)

def extract_data_from_csv()->None:
    columns = [
        "Rowid",
        "Timestamp",
        "Anonymized Vehicle number",
        "Vehicle type",
        "Number of axles",
        "Vehicle code"
    ]
    df = pd.read_csv(f"{PATH}/vehicle-data.csv", header=None,names=columns)
    data = df[["Rowid","Timestamp","Anonymized Vehicle number","Vehicle type"]]
    data.to_csv(f"{PATH}/csv_data.csv",index=False)

# extract_data_from_csv()

def extract_data_from_tsv()->None:
    columns = [
        "Rowid",
        "Timestamp",
        "Anonymized Vehicle number",
        "Vehicle type",
        "Number of axles",
        "Tollplaza id",
        "Tollplaza code"
    ]
    df = pd.read_csv(f"{PATH}/tollplaza-data.tsv",delimiter="\t", header=None,names=columns)
    data = df[["Number of axles","Tollplaza id","Tollplaza code"]]
    data.to_csv(f"{PATH}/tsv_data.csv",index=False)

def extract_data_from_fixed_width()->None:
    # df = pd.read_csv(f"{PATH}/payment-data.txt", sep='\\s+', header=None,names=columns)
    # print(df.head())
    
    # Aother method
    df_list = []
    columns = ["Type of Payment code","Vehicle code"]

    with open(f"{PATH}/payment-data.txt", 'r') as f:
        df = pd.DataFrame(columns=columns)
        for line in f.readlines():
            res = re.sub(r' +',",", line.strip()).split(',')[-2:]
            df = pd.concat([df,pd.DataFrame([res], columns=columns)])
        df = df.reset_index(drop=True)
        df.to_csv(f"{PATH}/fixed_width_data.csv", index=False)

def consolidate_data()->None:
    csv=pd.read_csv(f"{PATH}/csv_data.csv")
    tsv=pd.read_csv(f"{PATH}/tsv_data.csv")
    txt=pd.read_csv(f"{PATH}/fixed_width_data.csv")
    
    df = pd.concat([csv,tsv,txt],axis=1)
    df.to_csv(f"{PATH}/extracted_data.csv",index=False)

def transform_data()->None:
    df = pd.read_csv(f"{PATH}/extracted_data.csv")
    df['Vehicle type'] = df['Vehicle type'].str.upper()
    df.to_csv(f"{PATH}/transformed_data.csv",index=False)


default_args = {
    "owner": "nf_01",
    "start_date": datetime(2024,2,9),
    "retries" : 1
}

dag = DAG(
    dag_id="toll_data_python",
    description="DAG for tollplaza data using python",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False
)

download_dataset = PythonOperator(
    task_id="download_tar",
    python_callable=download_dataset,
    dag=dag
)
untar_dataset = PythonOperator(
    task_id="untar_dataset",
    python_callable=untar_dataset,
    dag=dag
)
extract_data_from_csv = PythonOperator(
    task_id="extract_data_from_csv",
    python_callable=extract_data_from_csv,
    dag=dag
)
extract_data_from_tsv = PythonOperator(
    task_id="extract_data_from_tsv",
    python_callable=extract_data_from_tsv,
    dag=dag
)
extract_data_from_fixed_width = PythonOperator(
    task_id="extract_data_from_fixed_width",
    python_callable=extract_data_from_fixed_width,
    dag=dag
)
consolidate_data = PythonOperator(
    task_id="consolidate_data",
    python_callable=consolidate_data,
    dag=dag
)
transform_data = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    dag=dag
)
cleanup = BashOperator(
    task_id="cleanup",
    bash_command=f"""
    cd {PATH} && rm csv_data.csv extracted_data.csv fixed_width_data.csv payment-data.txt tollplaza-data.tsv tsv_data.csv vehicle-data.csv fileformats.txt
    """,
    dag=dag
)

download_dataset >> untar_dataset >> [extract_data_from_csv,extract_data_from_tsv,extract_data_from_fixed_width] >> consolidate_data
consolidate_data >> transform_data >> cleanup