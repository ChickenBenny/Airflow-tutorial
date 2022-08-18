from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Benny',
    'retries': 5,
    'retries_delay': timedelta(minutes = 2)
}

def greet():
    print("Hello Airflow")


with DAG(
    dag_id = 'catchup',
    default_args = default_args,
    description = 'catchup',
    start_date = datetime(2022, 8, 16),
    schedule_interval = '@daily',
    catchup = True
) as dag:
    task1 = PythonOperator(
        task_id = 'task1',
        python_callable = greet,
    )


    task1
