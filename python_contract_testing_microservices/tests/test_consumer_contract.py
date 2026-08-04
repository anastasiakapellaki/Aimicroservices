import pytest
from unittest.mock import Mock, patch

from consumer.client import InvoiceConsumer


def _mock_response(data: dict) -> Mock:
    mock_resp = Mock()
    mock_resp.json.return_value = data
    mock_resp.raise_for_status = Mock()
    return mock_resp


CONTRACT_BODY = {
    "invoiceId": 1,
    "customerName": "Maria Papadopoulou",
    "amount": 120.5,
    "status": "PAID",
}


def test_consumer_parses_contract_response():
    """Consumer correctly maps the provider's contract JSON to InvoiceDto."""
    with patch("consumer.client.requests.get") as mock_get:
        mock_get.return_value = _mock_response(CONTRACT_BODY)
        invoice = InvoiceConsumer("http://provider:8000").get_invoice(1)

    assert invoice.invoiceId == 1
    assert invoice.customerName == "Maria Papadopoulou"
    assert invoice.amount == 120.5
    assert invoice.status == "PAID"


def test_contract_violation_renamed_field_breaks_consumer():
    """Breaking change: provider renames 'customerName' → 'customer' → consumer raises KeyError."""
    broken_body = {
        "invoiceId": 1,
        "customer": "Maria Papadopoulou",   # renamed — BREAKING CHANGE
        "amount": 120.5,
        "status": "PAID",
    }
    with patch("consumer.client.requests.get") as mock_get:
        mock_get.return_value = _mock_response(broken_body)
        with pytest.raises(KeyError):
            InvoiceConsumer("http://provider:8000").get_invoice(1)
