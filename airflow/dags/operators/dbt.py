import json
from airflow.utils.decorators import apply_defaults
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.utils.log.secrets_masker import mask_secret

class Dbt(BashOperator):
    """
    This class defines the dbt operator that's able to run dbt CLI against the database.
    This is needed because we need to set the profile & run dbt deps on every worker.
    """

    @apply_defaults
    def __init__(
            self,
            command,
            *args, **kwargs):

        # Set target
        target = 'dev'

        # Get profile vars from environment variables
        dbt_profile = json.loads(Variable.get(f'dbt-profile-{target}', default_var=''))

        # Mask secrets in the UI and in the logs
        mask_secret(dbt_profile['host'])
        mask_secret(dbt_profile['pass'])

        # Steps:
        # 1. Copy dbt project to /tmp folder
        # 2. Export required environment variables for profiles.yml
        # 3. Run dbt command
        #
        # Resources:
        # - AWS: https://docs.aws.amazon.com/mwaa/latest/userguide/samples-dbt.html
        super().__init__(bash_command=f"""
            cp -R /usr/local/airflow/dags/dbt_transformation /tmp;\
            export DBT_SCHEMA={dbt_profile['schema']};\
            export DBT_HOST={dbt_profile['host']};\
            export DBT_USER={dbt_profile['user']};\
            export DBT_PASSWORD={dbt_profile['pass']};\
            /usr/local/airflow/.local/bin/dbt deps --project-dir /tmp/dbt_transformation --profiles-dir /tmp/dbt_transformation --target {target};\
            /usr/local/airflow/.local/bin/dbt {command} --project-dir /tmp/dbt_transformation --profiles-dir /tmp/dbt_transformation --target {target};\
        """, *args, **kwargs)
        self.command = command
