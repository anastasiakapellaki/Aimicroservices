from dataclasses import dataclass
import requests


@dataclass
class InvoiceDto:
    invoiceId: int
    customerName: str
    amount: float
    status: str


class InvoiceConsumer:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_invoice(self, invoice_id: int) -> InvoiceDto:
        response = requests.get(f"{self.base_url}/invoices/{invoice_id}", timeout=5)
        response.raise_for_status()
        data = response.json()
        return InvoiceDto(
            invoiceId=data["invoiceId"],
            customerName=data["customerName"],
            amount=float(data["amount"]),
            status=data["status"],
        )
