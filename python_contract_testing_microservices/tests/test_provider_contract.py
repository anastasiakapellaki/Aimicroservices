import json

import pytest
from pydantic import ValidationError

from message_contracts.models import InvoiceCreated, InvoiceItems, InvoiceToCreate


def _produce_message(invoice_number: int = 55123) -> bytes:
    """Simulates the bytes that the producer publishes to RabbitMQ."""
    invoice = InvoiceCreated(
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
                )
            ],
        ),
    )
    return invoice.model_dump_json().encode("utf-8")


def test_consumer_deserializes_producer_message():
    """
    Verifies that the consumer can correctly deserialize the message
    published by the producer using the shared message contract.
    """
    body = _produce_message(invoice_number=55123)
    received = InvoiceCreated.model_validate_json(body)

    assert received.invoice_number == 55123
    assert received.invoice_data.customer_number == 12345
    assert received.invoice_data.invoice_items[0].price == 100.0


def test_contract_violation_renamed_field_breaks_consumer():
    """
    Breaking change demo: producer renames 'invoice_number' → 'id'.
    Consumer fails to parse → contract violation is detected before deployment.
    """
    broken_body = json.dumps({
        "id": 99999,          # renamed from invoice_number — BREAKING CHANGE
        "invoice_data": {
            "customer_number": 12345,
            "invoice_items": [],
        },
    }).encode("utf-8")

    with pytest.raises(ValidationError):
        InvoiceCreated.model_validate_json(broken_body)
