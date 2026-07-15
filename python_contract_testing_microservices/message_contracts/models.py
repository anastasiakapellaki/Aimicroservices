from __future__ import annotations

from typing import List

from pydantic import BaseModel


class InvoiceItems(BaseModel):
    description: str
    price: float
    actual_mileage: float
    base_rate: float
    is_oversized: bool
    is_refrigerated: bool
    is_hazardous_material: bool


class InvoiceToCreate(BaseModel):
    customer_number: int
    invoice_items: List[InvoiceItems]


class InvoiceCreated(BaseModel):
    invoice_number: int
    invoice_data: InvoiceToCreate
