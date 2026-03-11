import uuid

DATABASE = {
    "invoices": {}
}


def create_invoice(vendor_id: str, amount: float):
    invoice_id = str(uuid.uuid4())

    DATABASE["invoices"][invoice_id] = {
        "vendor_id": vendor_id,
        "amount": amount,
        "status": "draft"
    }

    return f"Invoice created: {invoice_id}"


def approve_invoice(invoice_id: str):
    invoice = DATABASE["invoices"].get(invoice_id)

    if not invoice:
        return "Invoice does not exist"

    if invoice["status"] != "draft":
        return "Only draft invoices can be approved"

    invoice["status"] = "approved"

    return f"Invoice {invoice_id} approved"