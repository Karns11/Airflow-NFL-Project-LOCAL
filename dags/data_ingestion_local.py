import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from scrapeNFLData import scrape_weekly_data
from ingestNFLData import ingest_weekly_data


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow")

POSTGRES_USER = os.getenv('MY_PG_USER')
POSTGRES_PASSWORD = os.getenv('MY_PG_PASSWORD')
PG_HOST = os.getenv('MY_PG_HOST')
PG_PORT = os.getenv('MY_PG_PORT')
POSTGRES_DB = os.getenv('MY_PG_DB')

CSV_NAME_TEMPLATE = AIRFLOW_HOME + '/weekly_nfl_data_{{ execution_date.strftime(\'%Y-%m-%d\') }}.csv'

TABLE_NAME = 'AF_Weekly_Nfl_Data'

current_year = '{{ execution_date.strftime(\'%Y\') }}'


local_workflow = DAG(
    "localNFLDataIngestionDag",
    schedule_interval="@daily",
    start_date=datetime(2024, 9, 21)
)


with local_workflow:

    scrape_data_task = PythonOperator(
        task_id='scrape',
        python_callable=scrape_weekly_data,
        op_kwargs=dict(
            csv_name= CSV_NAME_TEMPLATE,
            current_year=current_year
        ),
    )

    ingest_data_task = PythonOperator(
        task_id='ingestData',
        python_callable=ingest_weekly_data,
        op_kwargs=dict(
            user = POSTGRES_USER,
            password = POSTGRES_PASSWORD,
            host = PG_HOST,
            port = PG_PORT,
            db = POSTGRES_DB,
            csv_name = CSV_NAME_TEMPLATE,
            table_name = TABLE_NAME
        ),
    )

    # print_total_records_task = PythonOperator(
    #     task_id='printRecords',
    #     python_callable=print_records,
    #     op_kwargs=dict(
    #         user = POSTGRES_USER,
    #         password = POSTGRES_PASSWORD,
    #         host = PG_HOST,
    #         port = PG_PORT,
    #         db = POSTGRES_DB,
    #         table_name = TABLE_NAME
    #     ),
    # )

    scrape_data_task >> ingest_data_task #>> print_total_records_task