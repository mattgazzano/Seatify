from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

#Dags
with DAG('seatify_dag'
        ,start_date=datetime(2022,9,8)
        ,schedule_interval='@daily'
        ,dagrun_timeout=timedelta(minutes=60)
        ,catchup=False) as dag:
    
    task_extract_spotify_data = BashOperator(
        task_id='task_extract_spotify_data'
        , bash_command='python3 /home/mattgazzano/github/seatify/extract/spotify_ingestion.py'
    )

    task_extract_seatgeek_data = BashOperator(
        task_id='task_extract_seatgeek_data'
        , bash_command='python3 /home/mattgazzano/github/seatify/extract/seatgeek_ingestion.py'
    )

    task_ingestion_to_s3 = BashOperator(
        task_id='task_ingestion_to_s3'
        , bash_command='python3 /home/mattgazzano/github/seatify/load/ingestion_to_minio_s3.py'
    )

    task_s3_to_postgres = BashOperator(
        task_id = 'task_s3_to_postgres'
        , bash_command='python3 /home/mattgazzano/github/seatify/load/s3_to_postgres.py'
    )

task_extract_spotify_data >> task_extract_seatgeek_data >> task_ingestion_to_s3 >> task_s3_to_postgres