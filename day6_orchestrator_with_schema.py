from get_client import client
import json
import uuid
from typing import Literal,Optional
from pydantic import BaseModel,ValidationError,Field

MODEL_NAME = "models/gemini-2.5-flash"

MAX_RETRIES = 3

class CreateInvoiceCommand(BaseModel):
    action: Literal["create_invoice"]
    amount: float = Field(..., gt=0)

class ApproveInvoiceCommand(BaseModel):
    action: Literal["approve_invoice"]
    invoice_id: str

def validate_command(command_dict):
    action = command_dict.get("action")

    if action == "create_invoice":
        return CreateInvoiceCommand(**command_dict)

    elif action == "approve_invoice":
        return ApproveInvoiceCommand(**command_dict)

    else:
        raise ValueError("Unkown action")


DATABASE = {
    "invoices": {}
}


def validate_buisness(command):
    if isinstance(command,CreateInvoiceCommand):
        return True,"Valid"

    if isinstance(command,ApproveInvoiceCommand):
        invoice = DATABASE["invoices"].get(command.invoice_id)

        if not invoice:
            return False,"Invoice doesn't exist"

        if invoice["status"] != "draft":
            return False,"Only draft invoice can be approved"

        return True,"Valid"



def execute(command):
    if isinstance(command,CreateInvoiceCommand):
        invoice_id = str(uuid.uuid4())
        DATABASE["invoices"][invoice_id] = {
            "amount": command.amount,
            "status": "draft"
        }
        return f"Invoice created with ID {invoice_id}"

    if isinstance(command,ApproveInvoiceCommand):
        invoice_id = command.invoice_id
        DATABASE["invoices"][invoice_id]["status"] = "approved"
        return f"Invoice {invoice_id} approved"


SYSTEM_PROMPT = """
You are an ERP AI assistant.

Return ONLY valid JSON  without any markdown code fences.

Valid commands:

1) Create invoice:
{
  "action": "create_invoice",
  "amount": number greater than 0
}

2) Approve invoice:
{
  "action": "approve_invoice",
  "invoice_id": "string"
}

Do not include explanations.
Return raw JSON only.
"""

print("ERP Agent with Schema Validation (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    retries = 0
    feedback = ""

    while retries < MAX_RETRIES:

        prompt = SYSTEM_PROMPT + "\n"

        if feedback:
            prompt += f"Previous rejection: {feedback}\n"

        prompt += f"User request: {user_input}"

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        raw_text = response.text.strip()

        try:
            command_dict = json.loads(raw_text)
        except:
            print("Invalid JSON format.")
            break


        try:
            command=validate_command(command_dict)
        except ValidationError as e:
            print(f"Validation error: {e}")
            break

        is_valid,message = validate_buisness(command)
        if not is_valid:
            print(f"Rejected: {message}")
            feedback = message
            retries += 1
            continue

        result = execute(command)
        print("success:", result)
        break

    if retries == MAX_RETRIES:
        print("Escalation: Too many failed attempts. Human review required.\n")