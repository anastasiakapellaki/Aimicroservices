# Consumer Driven Contract Testing Microservices - Python Version

This project is a Python/FastAPI implementation of a simple Consumer Driven Contract Testing example.
It contains:

- `provider/`: Invoice Provider Microservice
- `consumer/`: Invoice Consumer client
- `contracts/`: JSON contract created from the consumer expectation
- `tests/`: Consumer and provider contract tests

## 1. Create virtual environment

```bash
python -m venv .venv
```

### Windows
```bash
.venv\Scripts\activate
```

### Linux/Mac
```bash
source .venv/bin/activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Run tests

```bash
pytest -v
```

Expected result:

```text
2 passed
```

## 4. Run provider microservice

```bash
uvicorn provider.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

Test endpoint:

```text
GET http://127.0.0.1:8000/invoices/1
```

Expected JSON:

```json
{
  "invoiceId": 1,
  "customerName": "Maria Papadopoulou",
  "amount": 120.5,
  "status": "PAID"
}
```

## Contract Testing Explanation

The consumer expects the provider to return an invoice with these fields:

- `invoiceId`: integer
- `customerName`: string
- `amount`: number
- `status`: string

The contract is stored in:

```text
contracts/invoice_contract.json
```

The provider contract test calls the real FastAPI provider using TestClient and validates that the response satisfies the consumer contract.

If the provider changes `customerName` to `clientName`, the test fails. This demonstrates how Consumer Driven Contract Testing detects breaking API changes before deployment.
