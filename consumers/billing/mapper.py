from typing import Any


def map_order_placed(event: dict[str, Any]) -> dict[str, Any]:
    customer = event["customer"]

    # TODO(student): replace these assumptions with a role-explicit v1 mapping.
    # v0 assumption: customer.id is the billing account and customer.address is invoice address.
    return {
        "billing_account": customer["id"],
        "invoice_address": customer["address"],
        "amount": event["acceptedTotal"],
        "currency": event["currency"],
    }
