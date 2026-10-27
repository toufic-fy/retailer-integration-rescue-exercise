import json

from consumers.common import EXCHANGE_NAME, connect_with_retry, decode_event
from consumers.crm.mapper import map_order_placed

QUEUE_NAME = "crm.order_placed"


def main() -> None:
    connection = connect_with_retry()
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout", durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME)

    def _on_message(ch, method, _properties, body: bytes) -> None:
        try:
            event = decode_event(body)
            dto = map_order_placed(event)
            print("[CRM] CustomerInteractionDTO")
            print(json.dumps(dto, indent=2))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as exc:  # noqa: BLE001
            print(f"[CRM] mapping failed: {exc}")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=_on_message)

    print("[CRM] waiting for events")
    channel.start_consuming()


if __name__ == "__main__":
    main()
