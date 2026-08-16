from typing import Any


def transform_customers(
    customers: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Clean and standardize customer records."""

    transformed = []
    seen_ids = set()

    for customer in customers:
        customer_id = str(
            customer["customer_id"]
        ).strip()

        if not customer_id:
            continue

        if customer_id in seen_ids:
            continue

        seen_ids.add(customer_id)

        transformed.append(
            {
                "customer_id": customer_id,
                "customer_name": str(
                    customer["customer_name"]
                ).strip(),
                "email": str(
                    customer["email"]
                ).strip().lower(),
                "city": str(
                    customer.get("city") or ""
                ).strip(),
                "country": str(
                    customer.get("country") or ""
                ).strip(),
                "signup_date": customer.get(
                    "signup_date"
                ),
            }
        )

    return transformed


def transform_orders(
    orders: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Clean orders and calculate total order amount."""

    transformed = []
    seen_ids = set()

    for order in orders:
        order_id = str(
            order["order_id"]
        ).strip()

        if not order_id:
            continue

        if order_id in seen_ids:
            continue

        seen_ids.add(order_id)

        quantity = int(order["quantity"])
        unit_price = float(order["unit_price"])

        if quantity <= 0 or unit_price < 0:
            continue

        total_amount = quantity * unit_price

        transformed.append(
            {
                "order_id": order_id,
                "customer_id": str(
                    order["customer_id"]
                ).strip(),
                "order_date": order["order_date"],
                "product": str(
                    order["product"]
                ).strip(),
                "category": str(
                    order.get("category") or ""
                ).strip(),
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": total_amount,
                "order_status": str(
                    order.get("order_status") or ""
                ).upper().strip(),
            }
        )

    return transformed
