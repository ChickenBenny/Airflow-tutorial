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

#we can pass the parameter either
def greetVar(name):
    print(f"Hello {name}")

with DAG(
    dag_id = 'python_Example',
    default_args = default_args,
    description = 'First python example dag.',
    start_date = datetime(2022, 8, 16),
    schedule_interval = '@daily'
) as dag:
    task1 = PythonOperator(
        #此operator未傳入參數
        task_id = 'task1',
        python_callable = greet,
    )

    task2 = PythonOperator(
        task_id = 'task2',
        python_callable = greetVar,
        op_kwargs = {"name": "Benny"}
    )


    task1
    task2