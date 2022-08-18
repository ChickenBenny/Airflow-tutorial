from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'Benny',
    'retries': 5,
    'retries_delay': timedelta(minutes = 2)
}


with DAG(
    dag_id = 'postgres_example',
    default_args = default_args,
    description = 'postgres_example',
    start_date = datetime(2022, 8, 18),
    schedule_interval = '0 0 * * *'
) as dag:
    task1 = PostgresOperator(
        task_id = 'Create_database',
        postgres_conn_id = 'postgres',
        sql = """
                CREATE TABLE IF NOT EXISTS dag_table(
                dt DATE PRIMARY KEY,
                id TEXT NOT NULL
                );
            """
    )

    task2 = PostgresOperator(
        task_id = 'Insert_data',
        postgres_conn_id = 'postgres',
        sql = """
                INSERT INTO dag_table (dt, id) VALUES ('{{ ds }}', '{{ dag.dag_id }}');
            """
    )

    task3 = PostgresOperator(
        task_id = 'Delete_data',
        postgres_conn_id = 'postgres',
        sql = """
                DELETE FROM dag_table WHERE dt = '{{ ds }}';    
            """
    )


    task1 >> task2 >> task3
