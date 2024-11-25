!/bin/bash

# Sync airflow/dags directory to S3
aws s3 sync airflow/dags s3://${AIRFLOW_BUCKET_NAME}/dags \
    --follow-symlinks --delete

# Zip airflow/plugins directory and upload to S3
zip -r - airflow/plugins | aws s3 cp - s3://${AIRFLOW_BUCKET_NAME}/plugins.zip

# Upload requirements.txt to S3
aws s3 cp requirements.txt s3://${AIRFLOW_BUCKET_NAME}/requirements.txt
