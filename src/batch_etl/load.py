import os
from typing import Any

import snowflake.connector


def get_snowflake_connection():
    """Create a connection to Snowflake."""

    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv(
            "SNOWFLAKE_WAREHOUSE"
        ),
        database=os.getenv(
            "SNOWFLAKE_DATABASE",
            "BATCH_ETL_DB",
        ),
        schema=os.getenv(
            "SNOWFLAKE_SCHEMA",
            "CURATED",
        ),
    )


def load_customers(
    customers: list[dict[str, Any]],
) -> int:
    """Load transformed customers into Snowflake."""

    connection = get_snowflake_connection()
    cursor = connection.cursor()

    try:
        for customer in customers:
            cursor.execute(
                """
                MERGE INTO DIM_CUSTOMER AS target
                USING (
                    SELECT
                        %s AS CUSTOMER_ID,
                        %s AS CUSTOMER_NAME,
                        %s AS EMAIL,
                        %s AS CITY,
                        %s AS COUNTRY,
                        %s AS SIGNUP_DATE
                ) AS source
                ON target.CUSTOMER_ID = source.CUSTOMER_ID

                WHEN MATCHED THEN UPDATE SET
                    CUSTOMER_NAME = source.CUSTOMER_NAME,
                    EMAIL = source.EMAIL,
                    CITY = source.CITY,
                    COUNTRY = source.COUNTRY,
                    SIGNUP_DATE = source.SIGNUP_DATE

                WHEN NOT MATCHED THEN INSERT (
                    CUSTOMER_ID,
                    CUSTOMER_NAME,
                    EMAIL,
                    CITY,
                    COUNTRY,
                    SIGNUP_DATE
                )
                VALUES (
                    source.CUSTOMER_ID,
                    source.CUSTOMER_NAME,
                    source.EMAIL,
                    source.CITY,
                    source.COUNTRY,
                    source.SIGNUP_DATE
                )
                """,
                (
                    customer["customer_id"],
                    customer["customer_name"],
                    customer["email"],
                    customer["city"],
                    customer["country"],
                    customer["signup_date"],
                ),
            )

        connection.commit()

        return len(customers)

    finally:
        cursor.close()
        connection.close()


def load_orders(
    orders: list[dict[str, Any]],
) -> int:
    """Load transformed orders into Snowflake."""

    connection = get_snowflake_connection()
    cursor = connection.cursor()

    try:
        for order in orders:
            cursor.execute(
                """
                MERGE INTO FACT_ORDERS AS target
                USING (
                    SELECT
                        %s AS ORDER_ID,
                        %s AS CUSTOMER_ID,
                        %s AS ORDER_DATE,
                        %s AS PRODUCT,
                        %s AS CATEGORY,
                        %s AS QUANTITY,
                        %s AS UNIT_PRICE,
                        %s AS TOTAL_AMOUNT,
                        %s AS ORDER_STATUS
                ) AS source
                ON target.ORDER_ID = source.ORDER_ID

                WHEN MATCHED THEN UPDATE SET
                    CUSTOMER_ID = source.CUSTOMER_ID,
                    ORDER_DATE = source.ORDER_DATE,
                    PRODUCT = source.PRODUCT,
                    CATEGORY = source.CATEGORY,
                    QUANTITY = source.QUANTITY,
                    UNIT_PRICE = source.UNIT_PRICE,
                    TOTAL_AMOUNT = source.TOTAL_AMOUNT,
                    ORDER_STATUS = source.ORDER_STATUS

                WHEN NOT MATCHED THEN INSERT (
                    ORDER_ID,
                    CUSTOMER_ID,
                    ORDER_DATE,
                    PRODUCT,
                    CATEGORY,
                    QUANTITY,
                    UNIT_PRICE,
                    TOTAL_AMOUNT,
                    ORDER_STATUS
                )
                VALUES (
                    source.ORDER_ID,
                    source.CUSTOMER_ID,
                    source.ORDER_DATE,
                    source.PRODUCT,
                    source.CATEGORY,
                    source.QUANTITY,
                    source.UNIT_PRICE,
                    source.TOTAL_AMOUNT,
                    source.ORDER_STATUS
                )
                """,
                (
                    order["order_id"],
                    order["customer_id"],
                    order["order_date"],
                    order["product"],
                    order["category"],
                    order["quantity"],
                    order["unit_price"],
                    order["total_amount"],
                    order["order_status"],
                ),
            )

        connection.commit()

        return len(orders)

    finally:
        cursor.close()
        connection.close()
