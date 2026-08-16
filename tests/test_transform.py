from batch_etl.transform import (
    transform_customers,
    transform_orders,
)


def test_transform_customer():
    customers = [
        {
            "customer_id": " C001 ",
            "customer_name": " Ravi Kumar ",
            "email": "RAVI@EXAMPLE.COM",
            "city": " Hyderabad ",
            "country": "India",
            "signup_date": "2025-01-10",
        }
    ]

    result = transform_customers(customers)

    assert len(result) == 1
    assert result[0]["customer_id"] == "C001"
    assert result[0]["customer_name"] == "Ravi Kumar"
    assert result[0]["email"] == "ravi@example.com"
    assert result[0]["city"] == "Hyderabad"


def test_duplicate_customers_are_removed():
    customers = [
        {
            "customer_id": "C001",
            "customer_name": "Ravi Kumar",
            "email": "ravi@example.com",
            "city": "Hyderabad",
            "country": "India",
            "signup_date": "2025-01-10",
        },
        {
            "customer_id": "C001",
            "customer_name": "Ravi Kumar",
            "email": "ravi@example.com",
            "city": "Hyderabad",
            "country": "India",
            "signup_date": "2025-01-10",
        },
    ]

    result = transform_customers(customers)

    assert len(result) == 1


def test_order_total_amount():
    orders = [
        {
            "order_id": "O1001",
            "customer_id": "C001",
            "order_date": "2025-05-01",
            "product": "Laptop",
            "category": "Electronics",
            "quantity": 2,
            "unit_price": 65000,
            "order_status": "completed",
        }
    ]

    result = transform_orders(orders)

    assert len(result) == 1
    assert result[0]["total_amount"] == 130000
    assert result[0]["order_status"] == "COMPLETED"


def test_duplicate_orders_are_removed():
    orders = [
        {
            "order_id": "O1001",
            "customer_id": "C001",
            "order_date": "2025-05-01",
            "product": "Laptop",
            "category": "Electronics",
            "quantity": 1,
            "unit_price": 65000,
            "order_status": "COMPLETED",
        },
        {
            "order_id": "O1001",
            "customer_id": "C001",
            "order_date": "2025-05-01",
            "product": "Laptop",
            "category": "Electronics",
            "quantity": 1,
            "unit_price": 65000,
            "order_status": "COMPLETED",
        },
    ]

    result = transform_orders(orders)

    assert len(result) == 1
