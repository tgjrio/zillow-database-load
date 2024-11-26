from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
from core.operators import process_zpids_for_sale

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'zillow_for_sale',
    default_args=default_args,
    description='DAG to fetch and process Zillow data with dynamic region support',
    schedule_interval=None,
    start_date=None,
    catchup=False,

) as dag:

    fetch_and_process_task = PythonOperator(
        task_id='extract-properties-for-sale',
        python_callable=process_zpids_for_sale,
        provide_context=True
    )

    trigger_downstream_dag = TriggerDagRunOperator(
        task_id='trigger-zillow-dataform',
        trigger_dag_id='zillow_dataform',
        wait_for_completion=True
    )

    fetch_and_process_task >> trigger_downstream_dag