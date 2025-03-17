from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator    
from manga_scrapper.manga_scrapper_concurrent import main
from manga_scrapper.store_images import fetch_and_download
from manga_scrapper.imgTopdf import final_convert_to_pdf


default_args = {
    'owner' : 'nf_01',
    "start_date" : datetime(2025, 3, 16),
    'retries' : 1
}

dag = DAG(
    dag_id="manga_scrapper",
    description="DAG for collect manga data",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup = False
    )

scrape_data_store_sqlite = PythonOperator(
    task_id="scrape_manga_webtoon",
    python_callable=main,
    dag=dag
)

download_manga_images = PythonOperator(
    task_id="download_images",
    python_callable=fetch_and_download,
    dag=dag
)

convert_images_to_pdf = PythonOperator(
    task_id="convert_imgs_to_pdf_each_chapter",
    python_callable=final_convert_to_pdf,
    dag=dag
)



scrape_data_store_sqlite >> download_manga_images >> convert_images_to_pdf