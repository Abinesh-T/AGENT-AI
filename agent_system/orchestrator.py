from schemas import CreateInvoiceCommand, ApproveInvoiceCommand
from tools import create_invoice, approve_invoice
from auth import authorize


def execute_command(command):

    authorize(command.action)

    if isinstance(command, CreateInvoiceCommand):
        return create_invoice(command.vendor_id, command.amount)

    if isinstance(command, ApproveInvoiceCommand):
        return approve_invoice(command.invoice_id)