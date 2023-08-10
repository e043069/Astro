"""
my_manatee_pipeline
DAG auto-generated by Astro Cloud IDE.
"""

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
import pendulum

import random

def num_manatees():
    aggregation_size = random.randint(1, 6)
    return f"This aggregation has {aggregation_size} manatees!"

@dag(
    schedule="0 0 * * *",
    start_date=pendulum.from_format("2023-08-03", "YYYY-MM-DD").in_tz("UTC"),
    catchup=False,
)
def my_manatee_pipeline():
    count_the_manatees = PythonOperator(
        python_callable=num_manatees,
        task_id="count_the_manatees",
    )

    name_the_baby_manatee = BashOperator(
        bash_command="echo \"The baby manatee's name is {{ var.value.MANATEE_NAME }}.\"",
        task_id="name_the_baby_manatee",
    )

    get_a_manatee_joke = SimpleHttpOperator(
        endpoint="manatees/random/",
        method="GET",
        http_conn_id="http_default",
        task_id="get_a_manatee_joke",
    )

    get_a_manatee_joke << name_the_baby_manatee

    name_the_baby_manatee << count_the_manatees

dag_obj = my_manatee_pipeline()
