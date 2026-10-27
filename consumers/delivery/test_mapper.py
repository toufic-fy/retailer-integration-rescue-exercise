from consumers.delivery.mapper import map_order_placed


def test_map_order_placed_happy_path() -> None:
    event = {
        "eventType": "OrderPlaced",
        "orderId": "ORD-184",
        "customer": {
            "id": "C-42",
            "name": "Lina Haddad",
            "address": "Hamra, Beirut",
            "status": "active",
        },
        "acceptedTotal": 126.0,
        "currency": "USD",
    }

    dto = map_order_placed(event)

    assert dto == {
        "recipient": "Lina Haddad",
        "delivery_address": "Hamra, Beirut",
        "order_reference": "ORD-184",
    }
