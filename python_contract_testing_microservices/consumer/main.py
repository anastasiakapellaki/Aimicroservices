import os
from fastapi import FastAPI, HTTPException
from consumer.client import InvoiceConsumer, InvoiceDto

app = FastAPI(title="Invoice Consumer Microservice")

PROVIDER_URL = os.getenv("PROVIDER_URL", "http://localhost:8000")


@app.get("/health")
def health_check():
    return {"status": "UP"}


@app.get("/invoice-summary/{invoice_id}", response_model=dict)
def invoice_summary(invoice_id: int):
    consumer = InvoiceConsumer(PROVIDER_URL)
    try:
        invoice: InvoiceDto = consumer.get_invoice(invoice_id)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return {
        "invoiceId": invoice.invoiceId,
        "customerName": invoice.customerName,
        "amount": invoice.amount,
        "status": invoice.status,
    }
