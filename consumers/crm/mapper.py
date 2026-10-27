from typing import Any


def map_order_placed(event: dict[str, Any]) -> dict[str, Any]:
    customer = event["customer"]

    # TODO(student): replace this assumption with owner-authoritative consent in v1.
    # v0 assumption: customer.status=active implies marketing eligibility.
    return {
        "contact": customer["name"],
        "marketing_eligible": customer["status"] == "active",
        "order_reference": event["orderId"],
    }
