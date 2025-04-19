# airflow/dags/profile_data_dag.py

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "you", # change
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
        dag_id="run_data_profiler",
        default_args=default_args,
        start_date=datetime(2024, 1, 1),
        schedule_interval="@daily",  # or "0 2 * * *"
        catchup=False
) as dag:

    run_profiler = BashOperator(
        task_id="run_profiler_script",
        bash_command="python D:\I\IdeaProjects\project_z\profiler\spark_profiler.py"
    )
