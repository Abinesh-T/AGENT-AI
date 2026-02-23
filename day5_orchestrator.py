import json
import uuid
from get_client import client

model_name = "models/gemini-2.5-flash"


max_retries = 3 

ALLOWED_TOOLS = ["create_invoice","approve_invoice"]

Database = {
    "invoices": []
}


def validate_command(command):
    action = command.get("action")

    if action not in ALLOWED_TOOLS:
        return False,"Action not allowed"

    if action == "create_invoice":
        if command.get("amount") <= 0:
            return False,"Invoice amount must be greate than zero"

    if action == "approve_invoice":
        invoice_id = command.get("invoice_id")
        invoice = Database["invoices"].get(invoice_id)

        if not invoice:
            return False,"Invoice doesn't exist"

        if invoice["amount"] <= 0:
            return False, "Invoice total cannot be zero"

        if invoice["status"] != "draft":
            return False, "Only draft invoice can be approved"

    return True, "Valid"


def execute_command(command):
    action = command["action"]

    if action == "create_invoice":
        invoice_id = str(uuid.uuid4())
        invoice_data = {
            "amount": command["amount"],
            "status": "draft"
        }
        # Since Database["invoices"] is a list, append a dict with id as a key
        Database["invoices"].append({"id": invoice_id, **invoice_data})
        return f"Invoice created with ID {invoice_id}"

    if action == "approve_invoice":
        invoice_id = command["invoice_id"]
        Database["invoices"][invoice_id]["status"] = "approved"
        return f"Invoice {invoice_id} approved"



SYSTEM_PROMPT = """
You are an ERP AI assistant.

Return only valid JSON in this format without any markdown code fences:

{
    "action":"<create_invoice | approve_invoice>",
    "amount":"<number if creating>",
    "invoice_id":"<id if approving>"
}
Amount and invoice_id are numbers.
Do not explain anything
Only return valid json.
"""


print("ERP Agent Orchestrator (type 'exit' to quit)\n")


while True:


    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    retries = 0
    feedback = ""

    while retries < max_retries:
        prompt = SYSTEM_PROMPT + "\n"

        if feedback:
            prompt += f"Previous rejection reason: {feedback}\n"

        prompt += f"User request: {user_input}"

        response = client.models.generate_content(
            model=model_name,
            contents = prompt
        )

        try:
            command = json.loads(response.text.strip())

        except:
            print("Failed to parse JSON.")
            break

        is_valid, message = validate_command(command)

        if not is_valid:
            print(f"Rejected: {message}")
            feedback = message
            retries += 1
            continue

        result = execute_command(command)
        print("success:", result)
        break

    if retries == max_retries:
        print("Escalation: Too many failed attempts. Human review required.\n")