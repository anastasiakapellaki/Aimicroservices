import random

import pika

from message_contracts.models import InvoiceCreated, InvoiceItems, InvoiceToCreate

QUEUE_NAME = "invoice-service"
EXCHANGE_NAME = "invoice-service"


def _build_sample_invoice(invoice_number: int) -> InvoiceCreated:
    return InvoiceCreated(
        invoice_number=invoice_number,
        invoice_data=InvoiceToCreate(
            customer_number=12345,
            invoice_items=[
                InvoiceItems(
                    description="Item 1",
                    price=100.0,
                    actual_mileage=50.0,
                    base_rate=10.0,
                    is_oversized=False,
                    is_refrigerated=False,
                    is_hazardous_material=False,
                ),
                InvoiceItems(
                    description="Item 2",
                    price=200.0,
                    actual_mileage=75.0,
                    base_rate=15.0,
                    is_oversized=True,
                    is_refrigerated=False,
                    is_hazardous_material=True,
                ),
            ],
        ),
    )


def publish_invoice(
    channel: pika.channel.Channel,
    invoice: InvoiceCreated,
    mode: str = "competing",
) -> None:
    body = invoice.model_dump_json().encode("utf-8")
    if mode == "competing":
        # Competing consumers: messages distributed across consumers
        channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=body)
    else:
        # Pub/Sub (fanout): every consumer gets its own copy
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key="", body=body)


def main() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # --- Competing consumers (direct queue) ---
    channel.queue_declare(queue=QUEUE_NAME, durable=False)

    # --- Pub/Sub fanout (uncomment to switch) ---
    # channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")

    print("Invoice Producer started. Press 'q' to exit or Enter to publish an invoice.")
    try:
        while True:
            key = input("> ").strip()
            if key.lower() == "q":
                break
            invoice_number = random.randint(10000, 99999)
            print(f"Created invoice with number: {invoice_number}")
            invoice = _build_sample_invoice(invoice_number)
            publish_invoice(channel, invoice)
            print(f"Published invoice {invoice_number} to queue '{QUEUE_NAME}'")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
