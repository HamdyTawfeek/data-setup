import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Default arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1)
}

# Create DAG
dag = DAG(
    'dbt_simple_pipeline',
    default_args=default_args,
    description='Run dbt models and tests',
    schedule_interval='0 5 * * *',
    catchup=False
)

# Define dbt project directory
DBT_PROJECT_DIR = os.environ.get("DBT_PROJECT_DIR", "/opt/airflow/dags/dbt_transformations")

# Create tasks
with dag:
    # Run dbt models
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run',
        cwd=DBT_PROJECT_DIR
    )

    # Run dbt tests
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='dbt test',
        cwd=DBT_PROJECT_DIR
    )

    # Set task dependencies
    dbt_run >> dbt_test