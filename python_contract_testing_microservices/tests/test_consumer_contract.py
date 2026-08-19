from pathlib import Path

from pact import Consumer, Provider

from consumer.client import InvoiceConsumer

PACT_DIR = str(Path(__file__).parent.parent / "pacts")
PACT_HOST = "localhost"
PACT_PORT = 1234

pact = Consumer("InvoiceConsumer").has_pact_with(
    Provider("InvoiceProvider"),
    host_name=PACT_HOST,
    port=PACT_PORT,
    pact_dir=PACT_DIR,
)


def test_get_invoice_matches_contract():
    """Consumer defines the interaction; Pact mock server verifies and writes the contract file."""
    expected_body = {
        "invoiceId": 1,
        "customerName": "Maria Papadopoulou",
        "amount": 120.50,
        "status": "PAID",
    }

    (
        pact.given("invoice 1 exists")
        .upon_receiving("a GET request for invoice 1")
        .with_request(method="GET", path="/invoices/1")
        .will_respond_with(200, body=expected_body)
    )

    with pact:
        invoice = InvoiceConsumer(f"http://{PACT_HOST}:{PACT_PORT}").get_invoice(1)

    assert invoice.invoiceId == 1
    assert invoice.customerName == "Maria Papadopoulou"
    assert invoice.amount == 120.50
    assert invoice.status == "PAID"
