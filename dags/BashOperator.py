from datetime import datetime, timedelta
from sched import scheduler
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Benny',
    'retries': 5,
    'retries_delay': timedelta(minutes = 2)
}

with DAG(
    dag_id = 'bash_Example',
    default_args = default_args,
    description = 'First bash example dag.',
    start_date = datetime(2022, 8, 16),
    schedule_interval = '@daily'
) as dag:
    task1 = BashOperator(
        task_id = 'task1',
        bash_command = "echo hello airflow"
    )

    task2 = BashOperator(
        task_id = 'task2',
        bash_command = "echo task 2 after task 1"
    )
    task3 = BashOperator(
        task_id = 'task3',
        bash_command = "echo task 3 after task 1"
    )
    task4 = BashOperator(
        task_id = 'task4',
        bash_command = "echo task 4 after task 2 and task 3"
    )


    task1 >> [task2, task3]
    [task2, task3] >> task4
