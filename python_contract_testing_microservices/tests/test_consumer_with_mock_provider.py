import json

from message_contracts.models import InvoiceCreated, InvoiceItems, InvoiceToCreate


def _sample_invoice(invoice_number: int = 42000) -> InvoiceCreated:
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
                )
            ],
        ),
    )


def test_producer_serializes_invoice_according_to_contract():
    """
    Verifies that the producer correctly serializes an InvoiceCreated
    message using the shared message contract (MessageContracts).
    """
    invoice = _sample_invoice(invoice_number=42000)
    payload = json.loads(invoice.model_dump_json())

    assert payload["invoice_number"] == 42000
    assert payload["invoice_data"]["customer_number"] == 12345
    assert len(payload["invoice_data"]["invoice_items"]) == 1

    item = payload["invoice_data"]["invoice_items"][0]
    assert item["description"] == "Item 1"
    assert item["price"] == 100.0
    assert item["is_oversized"] is False
    assert item["is_hazardous_material"] is False
