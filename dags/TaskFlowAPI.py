from datetime import datetime, timedelta
from airflow.decorators import dag, task


default_args = {
    'owner': 'Benny',
    'retries': 5,
    'retry_delay': timedelta(minutes = 2)
}

@dag(dag_id='task_flow_api', 
     default_args=default_args, 
     start_date=datetime(2022, 8, 16), 
     schedule_interval='@daily')
def example():

    @task(multiple_outputs = True)
    def get_name():
        return {
            'first_name': 'Benny',
            'last_name': 'Hsiao'
        }

    @task()
    def get_age():
        return 26

    @task()
    def greet(first_name, last_name, age):
        print(f"Hello is {first_name} {last_name}, I am {age} years old")
    
    name_dict = get_name()
    age = get_age()
    greet(first_name = name_dict['first_name'], 
          last_name = name_dict['last_name'],
          age = age)

greet_dag = example()