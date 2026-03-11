from pydantic import BaseModel, Field
from typing import Literal


class CreateInvoiceCommand(BaseModel):
    action: Literal["create_invoice"]
    vendor_id: str
    amount: float = Field(..., gt=0)


class ApproveInvoiceCommand(BaseModel):
    action: Literal["approve_invoice"]
    invoice_id: str