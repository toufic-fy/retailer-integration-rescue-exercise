# Retailer Integration Rescue Starter Kit

This workshop shows how technically valid events can still produce unsafe business outcomes when semantic roles are ambiguous.

## Stack

- Python 3.12
- RabbitMQ 3 Management
- pika
- Docker Compose
- pytest

## Project layout

- contracts: v0 and v1 event contracts
- events: publishable event payloads
- instructor_only: hidden truth for the revealing case
- order_management: event publisher
- consumers: Billing, Delivery, CRM consumers and mappers

## Run

1. Start infrastructure and consumers:

```bash
docker compose up --build -d
```

2. Publish happy-path event:

```bash
docker compose run --rm order-management python publisher.py /events/happy_path_v0.json
```

3. Inspect consumer output:

```bash
docker compose logs --tail=50 billing delivery crm
```

4. Publish revealing case:

```bash
docker compose run --rm order-management python publisher.py /events/revealing_case_v0.json
```

5. Inspect output again:

```bash
docker compose logs --tail=50 billing delivery crm
```

6. Tear down:

```bash
docker compose down -v
```

RabbitMQ Management UI: http://localhost:15672

- username: workshop
- password: workshop

## Student tasks

- Edit only mapper files under consumers:
  - consumers/billing/mapper.py
  - consumers/delivery/mapper.py
  - consumers/crm/mapper.py
- Make assumptions explicit for v0.
- Propose and map to a role-explicit v1 event.

## Tests

Run mapper tests locally:

```bash
python -m pytest consumers
```

## Packaging note

The instructor_only directory should be excluded from the student release archive.
