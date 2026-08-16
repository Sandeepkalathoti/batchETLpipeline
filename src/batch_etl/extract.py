import os
from typing import Any

import mysql.connector


def get_mysql_connection():
    """Create a connection to the MySQL source database."""

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        database=os.getenv(
            "MYSQL_DATABASE",
            "batch_etl_source",
        ),
    )


def extract_customers() -> list[dict[str, Any]]:
    """Extract customer records from MySQL."""

    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                customer_id,
                customer_name,
                email,
                city,
                country,
                signup_date
            FROM customers
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def extract_orders() -> list[dict[str, Any]]:
    """Extract order records from MySQL."""

    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                order_id,
                customer_id,
                order_date,
                product,
                category,
                quantity,
                unit_price,
                order_status
            FROM orders
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
