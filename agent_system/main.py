import json
import re
from get_client import client
from schemas import CreateInvoiceCommand, ApproveInvoiceCommand
from orchestrator import execute_command
from pydantic import ValidationError

MODEL_NAME = "models/gemini-2.5-flash"


SYSTEM_PROMPT = """
You are an ERP assistant.

Return ONLY raw JSON.

Commands:

Create invoice:
{
 "action": "create_invoice",
 "vendor_id": "string",
 "amount": number
}

Approve invoice:
{
 "action": "approve_invoice",
 "invoice_id": "string"
}
"""


def extract_json(raw: str) -> str:
    """Strip markdown code fences if the model wrapped JSON in ```json ... ```."""
    raw = raw.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw)
    if match:
        return match.group(1).strip()
    return raw


print("Safe Agent System\n")

while True:

    user_input = input("You: ")

    if user_input == "exit":
        break

    prompt = SYSTEM_PROMPT + "\nUser request: " + user_input

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
    except Exception as e:
        print("API error:", e)
        continue

    try:
        raw = response.text.strip()
    except (ValueError, AttributeError):
        raw = ""
    raw = extract_json(raw)

    if not raw:
        print("System error: No response from model (empty or blocked). Please try again.")
        continue

    try:
        command_dict = json.loads(raw)

        if "action" not in command_dict:
            print("Agent did not return a valid action.")
            continue

        if command_dict["action"] == "create_invoice":
            command = CreateInvoiceCommand(**command_dict)

        elif command_dict["action"] == "approve_invoice":
            command = ApproveInvoiceCommand(**command_dict)

        else:
            raise ValueError("Unknown action")

        result = execute_command(command)

        print("Result:", result)

    except json.JSONDecodeError as e:
        print("System error: Model did not return valid JSON.", e)

    except ValidationError as e:
        print("Schema validation error:", e)

    except PermissionError as e:
        print("Authorization error:", e)

    except Exception as e:
        print("System error:", e)