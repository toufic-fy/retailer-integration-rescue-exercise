import json
import time
from typing import Any

import pika

EXCHANGE_NAME = "retailer.events"
EVENT_TYPE = "OrderPlaced"
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


def decode_event(body: bytes) -> dict[str, Any]:
    payload = json.loads(body.decode("utf-8"))
    if payload.get("eventType") != EVENT_TYPE:
        raise ValueError(f"Unsupported eventType: {payload.get('eventType')}")
    return payload
