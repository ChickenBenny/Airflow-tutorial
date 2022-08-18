FROM apache/airflow:2.0.1
WORKDIR /
COPY ./requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install -r requirements.txt