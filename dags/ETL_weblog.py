from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
import os


os.makedirs("./data/", exist_ok=True)
PATH = "/opt/airflow/data/"

default_args = {
    'owner' : 'nf_01',
    "start_date" : datetime(2024, 2, 8),
    'email' : 'a.kumar01c@gmail.com'
}

dag = DAG(
    dag_id="process_web_log",
    description="process log",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup = False
)

download_data = BashOperator(
    task_id="download_data",
    bash_command=f"""
        cd {PATH} && curl https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/ETL/accesslog.txt > accesslog.txt
        """
)

extract_data = BashOperator(
    task_id="extract_data",
    bash_command=f"""
       cd {PATH} && cut -f1 -d" " accesslog.txt > extracted_data.txt
    """,
    dag=dag
)

transform_data = BashOperator(
    task_id="transform_data",
    bash_command=f"""
       cd {PATH} && grep -v "198.46.149.143" accesslog.txt > transformed_data.txt
    """,
    dag=dag
)

load_data = BashOperator(
    task_id="load_data",
    bash_command=f"""
       cd {PATH} && tar -cvf weblog.tar transformed_data.txt
    """,
    dag=dag
)

cleanup = BashOperator(
    task_id="cleanup",
    bash_command=f"""
    cd {PATH} && rm extracted_data.txt transformed_data.txt accesslog.txt
    """,
    dag=dag
)


download_data >> extract_data >> transform_data >> load_data >> cleanup