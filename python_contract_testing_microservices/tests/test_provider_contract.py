import json
from pathlib import Path

import jsonschema
import pytest
from fastapi.testclient import TestClient

from provider.main import app

client = TestClient(app)

_CONTRACT_PATH = Path(__file__).parent.parent / "contracts" / "invoice_contract.json"


def _load_schema() -> dict:
    return json.loads(_CONTRACT_PATH.read_text())["interaction"]["response"]["bodySchema"]


def test_provider_satisfies_contract():
    """Provider GET /invoices/1 returns 200 and a body that validates against the contract schema."""
    schema = _load_schema()
    response = client.get("/invoices/1")

    assert response.status_code == 200
    jsonschema.validate(instance=response.json(), schema=schema)


def test_contract_violation_detected_by_schema():
    """Breaking change: 'customerName' renamed to 'customer' fails schema validation."""
    schema = _load_schema()
    broken_body = {
        "invoiceId": 1,
        "customer": "Maria Papadopoulou",   # renamed — BREAKING CHANGE
        "amount": 120.5,
        "status": "PAID",
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=broken_body, schema=schema)
