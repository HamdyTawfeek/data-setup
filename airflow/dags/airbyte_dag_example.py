# 1. Retrieve the Airbyte Connection ID
# 2. Create an Airbyte connection in Airflow UI

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor


with DAG(dag_id='Airbyte-Dag',
         default_args={'owner': 'Rajesh'},
         schedule_interval='@daily',
         start_date=days_ago(1)
    ) as dag:

    trigger_sync= AirbyteTriggerSyncOperator(
        task_id='airbyte_money_json_example',
        airbyte_conn_id='airbyte_conn',  # this is the ID we created on Airflow
        connection_id='Your Connection ID', # Get this ID by following Step 2
        asynchronous=True,
    )

    monitor_sync = AirbyteJobSensor(
        task_id='airbyte_sensor_money_json_example',
        airbyte_conn_id='airbyte_conn', # this is the ID we created on Airflow
        airbyte_job_id= trigger_sync.output
    )
    
    trigger_sync >> monitor_sync