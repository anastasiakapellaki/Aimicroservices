from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Invoice Provider Microservice")


class Invoice(BaseModel):
    invoiceId: int
    customerName: str
    amount: float
    status: str


INVOICES = {
    1: Invoice(invoiceId=1, customerName="Maria Papadopoulou", amount=120.50, status="PAID"),
    2: Invoice(invoiceId=2, customerName="Nikos Georgiou", amount=89.90, status="PENDING"),
}


@app.get("/health")
def health_check():
    return {"status": "UP"}


@app.get("/invoices/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: int):
    invoice = INVOICES.get(invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice
