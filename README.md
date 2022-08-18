# Airflow(Chinese version)
In this project we run the airflow by docker and this is the Chinese version of README. You can either read the English version. 
### Quick start
1. 創建資料夾，並複製此專案。
```
$ mkdir airflow-tutorial && cd ./airflow-tutorial
$ git clone https://github.com/ChickenBenny/Airflow-tutorial
```
2. 使用```airflow-init``` 初始化database。
```
$ docker-compose up airflow-init
```
初始化結束後會得到 ```exited with code 0```
![](https://i.imgur.com/8DsZfJy.png)

3. 利用Compose架設airflow，並用```docker ps```查看架設狀況。
```
$ docker-compose up
$ docker ps
```
![](https://i.imgur.com/ErtBQSo.png)

4. 打開網頁前往```127.0.0.1:8080```登入Airflow，並可以開始使用Airflow。
> By default
帳號 : airflow
密碼 : airflow


**yaml的額外設定**
1. 若需要官方的範例，在```AIRFLOW__CORE__LOAD_EXAMPLES```的地方將```true```改成```true```。
2. scheduler和worker的interval、timeout、trigger和retries都能依照個人需求自行設定。 
3. airflow-init的部分```_AIRFLOW_WWW_USER_USERNAME```和```_AIRFLOW_WWW_USER_PASSWORD```能自行設定，若沒有設定，預設帳號密碼皆為```airflow```。

### What is Airflow?
Airflow 是一款由Airbnb於2014年開發的開元軟體，主要用於日常排程和監控工作流程。且由於Airflow 有提供UI 介面，因此能協助你以視覺化的方式，去釐清pipline裡任務間的相依性及獨立性，並且能在介面中察看log檔、觸發紀錄以及任務狀態。
![](https://i.imgur.com/pYFvNeb.png)

### Airflow與Crontab的差異
看到這裡，大家肯定有個疑問: 日常性的排程不是也能透過Crontab來執行嗎? 那位什麼我還需要學習airflow呢? 一開始的我也有這些疑問，直到深入了解Airflow後才發現他的強大之處。在此我先整理幾點使用Airflow的好處，看了之後絕對讓你直呼我想學Airflow!!

* **輕易理解任務間關係**
Airflow 將任務以DAG的方式去進行宣告及呈現，使得我們能夠清楚的知道各任務間的關係，好比A任務需要先做才能使B任務有data能夠運行。假若今天Workflow變大了，Crontab很難去釐清任務間的關係，可能會導致在下指令的時候變得複雜，並且容易出錯。

* **監控任務的狀態**
Airflow 提供audit log、任務狀態及觸發次數等介面，讓使用者能夠快速地理解任務的狀況。當workflow在某一個task觸發失敗時，Airflow也提供重試及警告的方式，讓使用者能夠快速解決問題。若今天Workflow裡的task很多，並且任務間都是有順序性的，假如其中一個任務觸發失敗了，Crontab並不會主動去重試，並且需要撰寫腳本來觸發警告，相較起Airfow著實是遜色許多。
![](https://i.imgur.com/kaYMu3w.png)


* **支援Python 語法**
其實有許多工程師是半路出家的，對於Linux的bash不是那麼的熟悉，因此對於撰寫Crontab感到頭疼。Airflow提供了Python的Operator，只要將需要觸發的任務寫成function，便能夠過airflow完成規律性的運作，並且也能夠傳遞參數進入任務當中。

* **UI 介面**
Airflow 提供了相當好用的UI 介面，使用時只需先定義好任務，也能在UI 中使用脫拉的方式去定義任務間的關係，如果今天突然發現某個任務的執行順序出錯了，也能夠快速透過UI去更改。更提供了擁有Domain但不會撰寫程式的人，能夠加入專案的開發並能夠提供適當的排程順序。
![](https://i.imgur.com/gSTSu3t.png)


### Directed Acyclic Graph(DAG)介紹
![](https://i.imgur.com/q5r10mO.png)

DAG是由多個nodes組成的有向無環圖。假設我們有四個任務，我們可以清楚透過Ariflow的UI理解，任務1必須先完成才能完成任務2,3，任務4必須要在最後才能完成。透過點選任務，也能設定任務間的順序及相關性。
![](https://i.imgur.com/ZZbSqbk.png)

*Notice: DAG中不存在Loop*

### Task
任務是組成Airflow裡能被執行的基本單位，並且可以在DAG中進行安排。Task主要被分成三大類:
1. **Operators** : 預先定義好的templates，我們可以利用這些templates定義任務建構出tasks. 常見的Operators主要分成兩大類，分別為BashOperator和PythonOperator。
2. **Sensors** : 主要用來等待及監測某任務的發生。
3. **TaskFlow-decorated(@task)** : Airflow2引進的API編寫方式，在後面會介紹撰寫方式。

### Task-lifecycle
![](https://i.imgur.com/XN5eFjV.png)
### Create Dag
看到這裡大家一定躍躍欲試，想知道該如何撰寫第一個DAG。其實方法很簡單，我們只要在dag的資料夾中新增py檔，docker便能透過設定好的volume，我們的scheduler便能監視所有的task，並且trigger任務。

### DAG file
#### Required imports
1. datetime => 用來定義執行的時間，以及任務重啟及間隔。
2. DAG => 須從airflow import DAG，藉此撰寫workflow。
3. Operator => import 使用到的Operators
```
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
```
#### DAG properties
撰寫DAG的時候會先定義一個default_args，再將其傳入DAG中，常用的參數如下:

```
default_args = {
    'owner': 'Benny',
    'depends_on_past': False,
    'start_date': datetime(2022,8,17),
    'email': ['Benny@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# define the DAG
dag = DAG(
    dag_id = 'id',
    default_args = default_args,
    description = 'description',
    schedule_interval = '@daily', # run every day
    catchup=False # do not perform a backfill of missing runs
)
```

### BashOperator
BashOperator是使用Bash shell去執行的，Operator終須包含任務的編號及執行的指令，範例如下:
```
task = BashOperator(
    task_id='task',
    bash_command='echo "Hello airflow"'
)

// output : Hello airflow
```
### PythonOperator
PythonOperator是呼叫py的function去執行的，因此要記得一定要將要做的任務用def的方式去撰寫，範例如下:
```
def greet():
    print("Hello World")

task1 = PythonOperator(
    task_id = 'first_task',
    python_callable = greet
)

// output : Hello world
```
Function傳入參數的範例如下，記得要將傳入的參數寫成字典的形式。
```
def greet(firstname, lastname):
    print("Hi {firstname} {lastname}!")

task1 = PythonOperator(
    task_id = 'first_task',
    python_callable = greet
    op_kwargs={'firstname': 'Benny', 'lastname': 'Hsaio'}
    
// output : Hi Benny Hsiao!
)
```

### Dependency of tasks
假設今天有4個任務，可以使用```>> or <<```來定義先後順序，也能使用```set_upstream or set_downstream```。

![](https://i.imgur.com/Nj6jvfD.png)

```
// method1
task1 >> [task2, task3]
task2 >> task4

// method2
task1 >> task2
task1 >> task3
task2 >> task4

// method3
task1.setdownstream(task2)
task1.setdownstream(task3)
task2.setdownstream(task4)
```


### Data sharing --Xcoms
在每次執行完任務後，airflow會自動將return的結果傳至Xcoms，讓任務可以透過Xcoms彼此溝通和串接參數。但要小心儲存或提取的資料都是存取在database當中，因此有容量上限。若是需要傳遞大量的資料，便不建議使用Xcoms這種方式。可以在UI介面中的Admin中找到Xcoms的入口:
![](https://i.imgur.com/5JYd3Be.png)


#### 將資料推到Xcoms
Airflow利用函式中的```return```或```ti.xcom_push(key=${key}, value=${value}```將資料推送到Xcoms中，並且採用key, value的方式進行儲存。
```
def push_name(ti):
    ti.xcom_push(key = 'first_name', value = 'Benny')
    ti.xcom_push(key = 'last_name', value = 'Hsiao')


def push_age():
    return 26
```
![](https://i.imgur.com/cUZ9lHj.png)

#### 將資料從Xcoms中拉下來
利用```ti.xcom_pull(task_ids = ${id}, key = ${key}```將資料從Xcoms中拉下。
```
def greet(ti):
    first_name = ti.xcom_pull(task_ids = 'task1', key = 'first_name')
    last_name = ti.xcom_pull(task_ids = 'task1', key = 'last_name')
    age = ti.xcom_pull(task_ids = 'task2', key = 'return_value')
    print(f"Hello {first_name} {last_name}, you are {age} years old.")
```
查看結果方式:
1. 點選要查看的任務
![](https://i.imgur.com/2KWTc1c.png)

2. 點選你的task
![](https://i.imgur.com/dUBptwe.png)

3. 查看log紀錄
![](https://i.imgur.com/pQlxSIl.png)

### Task Flow API - decorator
Task flow API 是使用@decorator的方式進行任務的撰寫，有使用過Flask或FastAPI的朋友們因該是很熟悉這種撰寫方式。有一點要特別注意的是在使用decorator的撰寫方式，可以不用定義任務間的關係，airflow會自動幫你計算任務間的關係，範例如下:
```
from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    'owner': 'Benny',
    'retries': 5,
    'retries_delay': timedelta(minutes = 2)
}

@dag(dag_id = 'Task Flow eg',
     default_args = default_args,
     start_data = datetime(2022, 8, 17))
def example_etl():

    @task
    def get_name(multi_outputs = True):
        return {
            "firstname": "Benny",
            "lastname": "Hsiao"
        }

    @task
    def get_age():
        return 26

    @task
    def greet(firstname, lastname, age):
        print(f"Hello {firstname} {lastname}, you are {age} years old.")

    
    dict_ = get_name()
    age = get_age
    greet(firstname = dict_['firstname'],
          lastname = dict_['lastname'],
          age = age)

example_etl = example_etl()
```
不用特別寫相關性，這點非常的方便，也能降低出錯的機會。

![](https://i.imgur.com/iihkCUB.png)

### Catch Up and Backfill
Catch up 可以幫助你檢視之後的任務排程，設定如下:
```
dag = DAG(
    dag_id = 'id',
    default_args = default_args,
    description = 'description',
    schedule_interval = '@daily', 
    catchup=True 
)
```
不過在這裡，我個人覺得Airflow UI提供的Calender跟其他的工具就很好用了，不用特別設定catchup。
![](https://i.imgur.com/ZkDAZ8a.png)

### schedule interval - cron expression
Airflow 的scheduler 會監控所有的任務及DAGs, 並且定期trigger任務。我們可以在DAG的properties中設定，scheduler多久會觸發一次這個任務，而定義的方式是使用cron expression去撰寫的。範例如下:
```
with DAG(
    dag_id = 'dag_id',
    default_args = default_args,
    description = 'dag_id',
    start_date = datetime(2022, 8, 16),
    schedule_interval = '@daily'
```
#### Cron expression
熟悉Crontab的平有因該對```@daily```或```* * * * *```的寫法不那麼陌生，不熟的朋友可以去[crontab guru](https://https://crontab.guru/)的網頁中玩玩看。想了解Crontab的朋友，也歡迎去[鳥站](https://https://linux.vbird.org/linux_basic/centos7/0430cron.php)閱讀相關的文章。在這邊提供一下常用的排程規則，如下:


| 排程規則 | 功能說明 | 
|:--------:|:--------:| 
|   @reboot   |   每次重新開機之後，執行一次。   | 
|   @reboot   |   每次重新開機之後，執行一次。   | 
|   @yearly   |   每年執行一次(0 0 1 1 *)。  | 
|   @annually   |   每年執行一次(0 0 1 1 *)。   | 
|   @monthly  |   每月執行一次(0 0 1 * *)。   | 
|   @weekly   |   每年執行一次(0 0 * * 0)。   | 
|   @daily   |   每年執行一次(0 0 * * *)。   | 
|   @hourly   |   每年執行一次(0 * * * *)。   |

### Airflow connection
在使用Airflow建立Workflow的時候，如果需要使連結到其他的服務，比如AWS的S3、MySQL server或者是PostgresSQL server，我們可以透過Airflow connection的方式去設定連結。並且在後續定義任務的時候，透過connection id來進行連線。以下以連接PostgreSQL為例，並透過task來建立table和插入資料。
1. 打開airflow的UI，透過Admin點選connection進入新增連結頁面。
![](https://i.imgur.com/NVRAzsk.png)
2. 進connection後，點選```+```進行新增，新增資訊如下:
![](https://i.imgur.com/wgmqw7x.png)
3. 撰寫DAG file
```
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

```
4. 至Airflow UI介面查看執行狀況，綠色即為成功，有興趣的朋友可以點及Log或進postgres的continer查看。
![](https://i.imgur.com/AAgJ4Nr.png)


#### Notice:
1. 如果Database是以docker的方式架設在本地端，Host的部分需可以填入yaml file中定義的名稱```postgres(我們yml定義的)```或是```host.docker.internal```。
2. 若是以local的方式運行，則直接填入localhost即可。
3. Postgres我預設的帳號、密碼及DB的名稱皆為airflow，若要修改可以治yaml file中進行編輯。
![](https://i.imgur.com/4JR1Vqt.png)

### 如何安裝Python套件
我們需要額外創建一個資料夾，在裡面新增```Dockerfile```和```requirements.txt```，將要新增的套件放在requirements中，接者修改yml即可。(把image的部分註解，使用build那行即可)
![](https://i.imgur.com/BMidnFA.png)

### 總結
* 學會如何使用Operator
* 學會如何建立task和DAG
* 學會如何連接其他服務

如果大家喜歡我的教程，歡迎幫我按星星!
