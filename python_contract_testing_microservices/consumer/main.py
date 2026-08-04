from consumer.client import InvoiceConsumer


def main() -> None:
    consumer = InvoiceConsumer("http://localhost:8000")
    invoice = consumer.get_invoice(1)
    print(f"Invoice #{invoice.invoiceId}: {invoice.customerName}, {invoice.amount}, {invoice.status}")


if __name__ == "__main__":
    main()
