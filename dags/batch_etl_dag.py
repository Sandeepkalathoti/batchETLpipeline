from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from batch_etl.extract import (
    extract_customers,
    extract_orders,
)
from batch_etl.transform import (
    transform_customers,
    transform_orders,
)
from batch_etl.quality import (
    validate_customers,
    validate_orders,
)


def extract_data(**context):
    customers = extract_customers()
    orders = extract_orders()

    context["ti"].xcom_push(
        key="customers",
        value=customers,
    )

    context["ti"].xcom_push(
        key="orders",
        value=orders,
    )


def transform_data(**context):
    customers = context["ti"].xcom_pull(
        task_ids="extract_data",
        key="customers",
    )

    orders = context["ti"].xcom_pull(
        task_ids="extract_data",
        key="orders",
    )

    transformed_customers = transform_customers(
        customers
    )

    transformed_orders = transform_orders(
        orders
    )

    context["ti"].xcom_push(
        key="customers",
        value=transformed_customers,
    )

    context["ti"].xcom_push(
        key="orders",
        value=transformed_orders,
    )


def quality_check(**context):
    customers = context["ti"].xcom_pull(
        task_ids="transform_data",
        key="customers",
    )

    orders = context["ti"].xcom_pull(
        task_ids="transform_data",
        key="orders",
    )

    valid_customers, invalid_customers = (
        validate_customers(customers)
    )

    valid_orders, invalid_orders = (
        validate_orders(orders)
    )

    print(
        f"Valid customers: {len(valid_customers)}"
    )

    print(
        f"Invalid customers: {len(invalid_customers)}"
    )

    print(
        f"Valid orders: {len(valid_orders)}"
    )

    print(
        f"Invalid orders: {len(invalid_orders)}"
    )

    if invalid_customers:
        print(
            "Invalid customer records:",
            invalid_customers,
        )

    if invalid_orders:
        print(
            "Invalid order records:",
            invalid_orders,
        )

    context["ti"].xcom_push(
        key="customers",
        value=valid_customers,
    )

    context["ti"].xcom_push(
        key="orders",
        value=valid_orders,
    )


def load_to_snowflake(**context):
    """
    Placeholder for Snowflake loading.

    Actual Snowflake loading is handled by
    the load module and will be enabled once
    Snowflake credentials are configured.
    """

    customers = context["ti"].xcom_pull(
        task_ids="quality_check",
        key="customers",
    )

    orders = context["ti"].xcom_pull(
        task_ids="quality_check",
        key="orders",
    )

    print(
        f"Customers ready for Snowflake: "
        f"{len(customers)}"
    )

    print(
        f"Orders ready for Snowflake: "
        f"{len(orders)}"
    )


default_args = {
    "owner": "data-engineering",
    "retries": 2,
}


with DAG(
    dag_id="batch_etl_pipeline",
    default_args=default_args,
    description="Daily batch ETL pipeline from MySQL to Snowflake",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=[
        "batch",
        "etl",
        "mysql",
        "snowflake",
    ],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    quality_task = PythonOperator(
        task_id="quality_check",
        python_callable=quality_check,
    )

    load_task = PythonOperator(
        task_id="load_to_snowflake",
        python_callable=load_to_snowflake,
    )

    (
        extract_task
        >> transform_task
        >> quality_task
        >> load_task
    )
