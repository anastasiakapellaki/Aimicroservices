import pika

from message_contracts.models import InvoiceCreated

QUEUE_NAME = "invoice-service"
EXCHANGE_NAME = "invoice-service"


def on_message(ch, method, properties, body: bytes) -> None:
    invoice = InvoiceCreated.model_validate_json(body)
    print(f" [x] Consumer 1 received invoice number: {invoice.invoice_number}")


def main() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # --- Competing consumers (direct queue) ---
    channel.queue_declare(queue=QUEUE_NAME, durable=False)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message, auto_ack=True)

    # --- Pub/Sub fanout (uncomment to switch) ---
    # channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")
    # result = channel.queue_declare(queue="", exclusive=True)
    # queue_name = result.method.queue
    # channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)
    # channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)

    print(f" [*] Consumer 1 waiting for messages on '{QUEUE_NAME}'. Press CTRL+C to exit.")
    channel.start_consuming()


if __name__ == "__main__":
    main()
