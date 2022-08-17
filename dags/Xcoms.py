from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Benny',
    'retries': 5,
    'retries_delay': timedelta(minutes = 2)
}



def push_name(ti):
    ti.xcom_push(key = 'first_name', value = 'Benny')
    ti.xcom_push(key = 'last_name', value = 'Hsiao')


def push_age():
    return 26

def greet(ti):
    first_name = ti.xcom_pull(task_ids = 'task1', key = 'first_name')
    last_name = ti.xcom_pull(task_ids = 'task1', key = 'last_name')
    age = ti.xcom_pull(task_ids = 'task2', key = 'return_value')
    print(f"Hello {first_name} {last_name}, you are {age} years old.")

with DAG(
    dag_id = 'Xcoms_Example',
    default_args = default_args,
    description = 'XcomS Example.',
    start_date = datetime(2022, 8, 16),
    schedule_interval = '@daily'
) as dag:
    task1 = PythonOperator(
        task_id = 'task1',
        python_callable = push_name
    )

    task2 = PythonOperator(
        task_id = 'task2',
        python_callable = push_age
    ) 
       
    task3 = PythonOperator(
        task_id = 'task3',
        python_callable = greet
    ) 


    [task1, task2] >> task3
