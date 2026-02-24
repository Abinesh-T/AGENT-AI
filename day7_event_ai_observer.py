from get_client import client
from decimal import Decimal
import uuid
import json
import datetime

model_name = "models/gemini-2.5-flash"

DATABASE = {
    "invoices": {}
}

EVENT_LOG = []

def emit_event(event_type,payload):
    event = {
        "event_id": str(uuid.uuid4()),
        "type": event_type,
        "payload": payload,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    EVENT_LOG.append(event)
    return event

def create_invoice(amount, vendor):
    invoice_id = str(uuid.uuid4())
    DATABASE["invoices"][invoice_id] = {
        "amount": Decimal(amount),
        "vendor": vendor,
        "status": "draft"
    }

    event = emit_event("invoice_created", {
        "invoice_id": invoice_id,
        "amount": str(amount),
        "vendor": vendor
    })

    return invoice_id, event

# -------------------------
# AI Observer
# -------------------------

SYSTEM_PROMPT = """
You are an ERP AI risk analyst.

You will receive a domain event.

Your job is to:
- Analyze risk
- Detect anomalies
- Suggest review if necessary

Do NOT suggest execution of financial actions.
Only return advisory analysis in plain text.
"""


def ai_analyze_event(event):

    prompt = SYSTEM_PROMPT + "\n\nEvent:\n" + json.dumps(event)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    return response.text


# -------------------------
# Simulation
# -------------------------

print("Event-Driven ERP AI Observer\n")

while True:
    amount = input("Enter invoice amount (or 'exit'): ")

    if amount.lower() == "exit":
        break

    vendor = input("Enter vendor name: ")

    invoice_id, event = create_invoice(amount, vendor)

    print("\nInvoice Created:", invoice_id)

    print("\nAI Advisory:")
    advisory = ai_analyze_event(event)
    print(advisory)

    print("\n---------------------------\n")