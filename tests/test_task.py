import pytest
from airflow.models import DagBag

@pytest.fixture(scope="session")
def dagbag():
    return DagBag(dag_folder='../airflow/dags')

def test_dag_loading(dagbag):
    assert len(dagbag.dags) > 0
