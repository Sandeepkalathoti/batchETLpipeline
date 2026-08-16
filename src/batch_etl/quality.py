from typing import Any


def validate_customers(
    customers: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Separate valid and invalid customer records."""

    valid = []
    invalid = []

    for customer in customers:
        errors = []

        if not customer.get("customer_id"):
            errors.append("Missing customer_id")

        if not customer.get("customer_name"):
            errors.append("Missing customer_name")

        if not customer.get("email"):
            errors.append("Missing email")

        if errors:
            invalid.append(
                {
                    "record": customer,
                    "errors": errors,
                }
            )
        else:
            valid.append(customer)

    return valid, invalid


def validate_orders(
    orders: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Separate valid and invalid order records."""

    valid = []
    invalid = []

    seen_order_ids = set()

    for order in orders:
        errors = []

        order_id = order.get("order_id")

        if not order_id:
            errors.append("Missing order_id")

        elif order_id in seen_order_ids:
            errors.append("Duplicate order_id")

        seen_order_ids.add(order_id)

        if not order.get("customer_id"):
            errors.append("Missing customer_id")

        if not order.get("product"):
            errors.append("Missing product")

        if order.get("quantity", 0) <= 0:
            errors.append(
                "Quantity must be greater than 0"
            )

        if order.get("unit_price", 0) < 0:
            errors.append(
                "Unit price cannot be negative"
            )

        if errors:
            invalid.append(
                {
                    "record": order,
                    "errors": errors,
                }
            )
        else:
            valid.append(order)

    return valid, invalid
