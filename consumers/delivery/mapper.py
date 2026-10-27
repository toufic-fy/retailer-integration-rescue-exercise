from typing import Any


def map_order_placed(event: dict[str, Any]) -> dict[str, Any]:
    customer = event["customer"]

    # TODO(student): replace these assumptions with a role-explicit v1 mapping.
    # v0 assumption: customer.name is the recipient and customer.address is delivery address.
    return {
        "recipient": customer["name"],
        "delivery_address": customer["address"],
        "order_reference": event["orderId"],
    }
