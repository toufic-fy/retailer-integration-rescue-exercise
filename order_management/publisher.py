import json
import sys
import time
from pathlib import Path

import pika

EXCHANGE_NAME = "retailer.events"
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "workshop"
RABBITMQ_PASS = "workshop"
RETRY_SECONDS = 2


def connect_with_retry() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

    while True:
        try:
            params = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                credentials=credentials,
                heartbeat=30,
            )
            return pika.BlockingConnection(params)
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying in 2 seconds...")
            time.sleep(RETRY_SECONDS)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python publisher.py /events/<event-file>.json")
        return 1

    event_path = Path(sys.argv[1])
    with event_path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)

    connection = connect_with_retry()
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout", durable=True)

    body = json.dumps(payload).encode("utf-8")
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key="",
        body=body,
        properties=pika.BasicProperties(delivery_mode=2),
    )
    print(f"Published event file: {event_path}")

    connection.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
