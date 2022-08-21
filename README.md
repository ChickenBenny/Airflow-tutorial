# Airflow(Chinese version)
### Quick start
1. 創建資料夾，並複製此專案。
```
$ mkdir airflow-tutorial && cd ./airflow-tutorial
$ git clone https://github.com/ChickenBenny/Airflow-tutorial
```
2. 使用```airflow-init``` 初始化 database。
```
$ docker-compose up airflow-init
```
初始化結束後會得到 ```exited with code 0```
![](https://i.imgur.com/8DsZfJy.png)

3. 利用 Compose 架設 airflow，並用```docker ps```查看架設狀況。
```
$ docker-compose up
$ docker ps
```
![](https://i.imgur.com/ErtBQSo.png)

4. 打開網頁前往```127.0.0.1:8080```登入 Airflow，並可以開始使用 Airflow。
> By default
帳號 : airflow
密碼 : airflow


**yaml的額外設定**
1. 若需要官方的範例，在```AIRFLOW__CORE__LOAD_EXAMPLES```的地方將```true```改成```true```。
2. scheduler 和 worker 的 interval、timeout、trigger 和 retries 都能依照個人需求自行設定。
3. airflow-init 的部分```_AIRFLOW_WWW_USER_USERNAME```和```_AIRFLOW_WWW_USER_PASSWORD```能自行設定，若沒有設定，預設帳號密碼皆為```airflow```。

### What is Airflow?
Airflow 是一款由 Airbnb 於 2014 年開發的開元軟體，主要用於日常排程和監控工作流程。且由於 Airflow 有提供 UI
介面，因此能協助你以視覺化的方式，去釐清 pipline 裡任務間的相依性及獨立性，並且能在介面中察看 log 檔、觸發紀錄以及任務狀態。
![](https://i.imgur.com/pYFvNeb.png)

### Airflow 與 Crontab 的差異
看到這裡，大家肯定有個疑問: 日常性的排程不是也能透過 Crontab 來執行嗎? 那位什麼我還需要學習 airflow 呢?
一開始的我也有這些疑問，直到深入了解 Airflow 後才發現他的強大之處。在此我先整理幾點使用 Airflow 的好處，看了之後絕對讓你直呼我想學 Airflow !!

* **輕易理解任務間關係**  
  Airflow 將任務以 DAG 的方式去進行宣告及呈現，使得我們能夠清楚的知道各任務間的關係，好比 A 任務需要先做才能使 B 任務有 data 能夠運行。
  假若今天 Workflow 變大了，Crontab 很難去釐清任務間的關係，可能會導致在下指令的時候變得複雜，並且容易出錯。

* **監控任務的狀態**  
  Airflow 提供 audit log、任務狀態及觸發次數等介面，讓使用者能夠快速地理解任務的狀況。當 workflow 在某一個
  task 觸發失敗時，Airflow 也提供重試及警告的方式，讓使用者能夠快速解決問題。
  若今天 Workflow 裡的 task很多，並且任務間都是有順序性的，假如其中一個任務觸發失敗了，Crontab 並不會主動去重試，並且需要撰寫腳本來觸發警告，相較起 Airfow 著實是遜色許多。
  ![](https://i.imgur.com/kaYMu3w.png)


* **支援Python 語法**  
  其實有許多工程師是半路出家的，對於 Linux 的 bash 不是那麼的熟悉，因此對於撰寫 Crontab 感到頭疼。
  Airflow 提供了 Python 的 Operator，只要將需要觸發的任務寫成 function，便能夠過 airflow 完成規律性的運作，並且也能夠傳遞參數進入任務當中。

* **UI 介面**  
  Airflow 提供了相當好用的 UI 介面，使用時只需先定義好任務，也能在 UI 中使用脫拉的方式去定義任務間的關係。
  如果今天突然發現某個任務的執行順序出錯了，也能夠快速透過 UI 去更改。更提供了擁有 Domain 但不會撰寫程式的人，能夠加入專案的開發並能夠提供適當的排程順序。
  ![](https://i.imgur.com/gSTSu3t.png)


### Directed Acyclic Graph(DAG)介紹
![](https://i.imgur.com/q5r10mO.png)

DAG 是由多個 nodes 組成的有向無環圖。假設我們有四個任務，我們可以清楚透過 Airflow 的 UI 理解，任務 1 必須先完成才能完成任務 2, 3，任務 4 必須要在最後才能完成。透過點選任務，也能設定任務間的順序及相關性。
![](https://i.imgur.com/ZZbSqbk.png)

*Notice: DAG 中不存在 Loop*

### Task
任務是組成 Airflow 裡能被執行的基本單位，並且可以在 DAG 中進行安排。Task 主要被分成三大類:
1. **Operators** :   
   預先定義好的 templates，我們可以利用這些 templates 定義任務建構出 tasks 常見的 Operators 主要分成兩大類，分別為 BashOperator 和 PythonOperator。
2. **Sensors** :   
   主要用來等待及監測某任務的發生。
3. **TaskFlow-decorated(@task)** :   
   Airflow2 引進的 API 編寫方式，在後面會介紹撰寫方式。

### Task-lifecycle
![](https://i.imgur.com/XN5eFjV.png)
### Create Dag
看到這裡大家一定躍躍欲試，想知道該如何撰寫第一個 DAG。
其實方法很簡單，我們只要在 dag 的資料夾中新增 `.py` 檔，docker 便能透過設定好的 volume，我們的 scheduler 便能監視所有的 task，並且啟動任務。

### DAG file
#### Required imports
1. datetime => 用來定義執行的時間，以及任務重啟及間隔。
2. DAG => 須從 airflow import DAG，藉此撰寫 workflow。
3. Operator => import 使用到的 Operators
```
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
```
#### DAG properties
撰寫 DAG 的時候會先定義一個 default_args，再將其傳入 DAG 中，常用的參數如下:

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
BashOperator 是使用 Bash shell 去執行的，Operator 終須包含任務的編號及執行的指令，範例如下:
```
task = BashOperator(
    task_id='task',
    bash_command='echo "Hello airflow"'
)

// output : Hello airflow
```
### PythonOperator
PythonOperator 是呼叫 py 的 function 去執行的，因此要記得一定要將要做的任務用 def 的方式去撰寫，範例如下:
```
def greet():
    print("Hello World")

task1 = PythonOperator(
    task_id = 'first_task',
    python_callable = greet
)

// output : Hello world
```
Function 傳入參數的範例如下，記得要將傳入的參數寫成字典的形式。
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
假設今天有 4 個任務，可以使用```>> or <<```來定義先後順序，也能使用```set_upstream or set_downstream```。

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
在每次執行完任務後，airflow 會自動將 return 的結果傳至 Xcoms，讓任務可以透過 Xcoms 彼此溝通和串接參數。但要小心儲存或提取的資料都是存取在 database
當中，因此有容量上限。若是需要傳遞大量的資料，便不建議使用 Xcoms 這種方式。可以在 UI 介面中的 Admin 中找到 Xcoms 的入口:
![](https://i.imgur.com/5JYd3Be.png)


#### 將資料推到 Xcoms
Airflow 利用函式中的```return```或```ti.xcom_push(key=${key}, value=${value}```將資料推送到 Xcoms 中，並且採用 key, value 的方式進行儲存。
```
def push_name(ti):
    ti.xcom_push(key = 'first_name', value = 'Benny')
    ti.xcom_push(key = 'last_name', value = 'Hsiao')


def push_age():
    return 26
```
![](https://i.imgur.com/cUZ9lHj.png)

#### 將資料從 Xcoms 中拉下來
利用```ti.xcom_pull(task_ids = ${id}, key = ${key}```將資料從 Xcoms 中拉下。
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

2. 點選你的 task
   ![](https://i.imgur.com/dUBptwe.png)

3. 查看 log 紀錄
   ![](https://i.imgur.com/pQlxSIl.png)

### Task Flow API - decorator
Task flow API 是使用 `@decorator` 的方式進行任務的撰寫，有使用過 Flask 或 FastAPI 的朋友們因該是很熟悉這種撰寫方式。有一點要特別注意的是在使用 decorator
的撰寫方式，可以不用定義任務間的關係，airflow 會自動幫你計算任務間的關係，範例如下:
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
不過在這裡，我個人覺得 Airflow UI 提供的 Calender 跟其他的工具就很好用了，不用特別設定 catchup。
![](https://i.imgur.com/ZkDAZ8a.png)

### schedule interval - cron expression
Airflow 的 scheduler 會監控所有的任務及 DAGs, 並且定期 trigger 任務。我們可以在 DAG 的 properties 中設定，scheduler 多久會觸發一次這個任務，而定義的方式是使用 cron
expression 去撰寫的。範例如下:
```
with DAG(
    dag_id = 'dag_id',
    default_args = default_args,
    description = 'dag_id',
    start_date = datetime(2022, 8, 16),
    schedule_interval = '@daily'
```
#### Cron expression
熟悉 Crontab 的平有因該對```@daily```或```* * * * *```的寫法不那麼陌生，不熟的朋友可以去 [crontab guru](https://crontab.guru)
的網頁中玩玩看。想了解 Crontab 的朋友，也歡迎去 [鳥站](https://https://linux.vbird.org/linux_basic/centos7/0430cron.php)
閱讀相關的文章。在這邊提供一下常用的排程規則，如下:

<table>
  <tr>
    <th>排程規則</th>
    <th>功能說明</th>
  </tr>
  <tr>
    <td>@reboot</td>
    <td>每次重新開機之後，執行一次</td>
  </tr>
  <tr>
    <td>@yearly</td>
    <td>每年執行一次 (0 0 1 1 *)</td>
  </tr>
  <tr>
    <td>@annually</td>
    <td>每年執行一次 (0 0 1 1 *)</td>
  </tr>
  <tr>
    <td>@monthly</td>
    <td>每月執行一次 (0 0 1 * *)</td>
  </tr>
  <tr>
    <td>@weekly</td>
    <td>每年執行一次 (0 0 * * 0)</td>
  </tr>
  <tr>
    <td>@daily</td>
    <td>每天執行一次 (0 0 * * *)</td>
  </tr>
  <tr>
    <td>@hourly</td>
    <td>每小時執行一次(0 * * * *)</td>
  </tr>
</table> 

### Airflow connection
在使用 Airflow 建立 Workflow 的時候，如果需要使連結到其他的服務，比如 AWS 的 S3、MySQL server 或者是 PostgresSQL server，我們可以透過 Airflow
connection 的方式去設定連結。並且在後續定義任務的時候，透過 connection id 來進行連線。以下以連接 PostgreSQL 為例，並透過 task 來建立 table 和插入資料。
1. 打開 airflow 的 UI，透過 Admin 點選 connection 進入新增連結頁面。
   ![](https://i.imgur.com/NVRAzsk.png)
2. 進 connection 後，點選```+```進行新增，新增資訊如下:
   ![](https://i.imgur.com/wgmqw7x.png)
3. 撰寫 DAG file
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
4. 至 Airflow UI 介面查看執行狀況，綠色即為成功，有興趣的朋友可以點及 Log 或進 postgres 的 container 查看。
   ![](https://i.imgur.com/AAgJ4Nr.png)


#### Notice:
1. 如果 Database 是以 docker 的方式架設在本地端，Host 的部分需可以填入 yaml file 中定義的名稱```postgres(我們yml定義的)```或是```host.docker.internal```。
2. 若是以 local 的方式運行，則直接填入 localhost 即可。
3. Postgres 我預設的帳號、密碼及 DB 的名稱皆為 airflow，若要修改可以治 yaml file 中進行編輯。
   ![](https://i.imgur.com/4JR1Vqt.png)

### 如何安裝 Python 套件
我們需要額外創建一個資料夾，在裡面新增```Dockerfile```和```requirements.txt```，
將要新增的套件放在 requirements 中，接者修改 yml 即可。(把 image 的部分註解，使用 build 那行即可)
![](https://i.imgur.com/BMidnFA.png)

### 總結
* 學會如何使用 Operator
* 學會如何建立 task 和 DAG
* 學會如何連接其他服務

如果大家喜歡我的教程，歡迎幫我按星星!