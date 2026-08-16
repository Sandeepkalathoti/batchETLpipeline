from batch_etl.quality import (
    validate_customers,
    validate_orders,
)


def valid_customer():
    return {
        "customer_id": "C001",
        "customer_name": "Ravi Kumar",
        "email": "ravi@example.com",
        "city": "Hyderabad",
        "country": "India",
        "signup_date": "2025-01-10",
    }


def valid_order():
    return {
        "order_id": "O1001",
        "customer_id": "C001",
        "order_date": "2025-05-01",
        "product": "Laptop",
        "category": "Electronics",
        "quantity": 1,
        "unit_price": 65000,
        "total_amount": 65000,
        "order_status": "COMPLETED",
    }


def test_valid_customer():
    valid, invalid = validate_customers(
        [valid_customer()]
    )

    assert len(valid) == 1
    assert len(invalid) == 0


def test_missing_customer_id():
    customer = valid_customer()
    customer["customer_id"] = ""

    valid, invalid = validate_customers(
        [customer]
    )

    assert len(valid) == 0
    assert len(invalid) == 1
    assert "Missing customer_id" in invalid[0]["errors"]


def test_missing_customer_name():
    customer = valid_customer()
    customer["customer_name"] = ""

    valid, invalid = validate_customers(
        [customer]
    )

    assert len(valid) == 0
    assert len(invalid) == 1
    assert "Missing customer_name" in invalid[0]["errors"]


def test_valid_order():
    valid, invalid = validate_orders(
        [valid_order()]
    )

    assert len(valid) == 1
    assert len(invalid) == 0


def test_duplicate_order():
    order = valid_order()

    valid, invalid = validate_orders(
        [order, order.copy()]
    )

    assert len(valid) == 1
    assert len(invalid) == 1
    assert "Duplicate order_id" in invalid[0]["errors"]


def test_invalid_quantity():
    order = valid_order()
    order["quantity"] = 0

    valid, invalid = validate_orders(
        [order]
    )

    assert len(valid) == 0
    assert len(invalid) == 1
    assert (
        "Quantity must be greater than 0"
        in invalid[0]["errors"]
    )


def test_negative_unit_price():
    order = valid_order()
    order["unit_price"] = -100

    valid, invalid = validate_orders(
        [order]
    )

    assert len(valid) == 0
    assert len(invalid) == 1
    assert (
        "Unit price cannot be negative"
        in invalid[0]["errors"]
    )
