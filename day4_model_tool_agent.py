from get_client import client
from day3_tool_agent import calculator
import json

model_name = "models/gemini-2.5-flash"

def calculator(expression: str):
    try:
        return str(eval(expression))
    except Exception:
        return "invalid math expression."


SYSTEM_PROMPT = """
You are an intelligent agent.


Decide whether to user input requires a calculator tool.

if it is a math expression, response only in the JSON format:
    {
    "action":"calculator",
    "input":"<math_expression>"
    }

if not tool is needed, respond only in this JSON format:
    {
    "action":"none",
    "input":"<original_user_input>"
    }

Do not include explanations.
Only return valid json.
"""

print("Model Tool Agent (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = client.models.generate_content(
        model=model_name,
        contents=SYSTEM_PROMPT + "\n User: " + user_input,
    )


    decision_text = response.text.strip()

    try:
        decision = json.loads(decision_text)
    except json.JSONDecodeError:
        print("Bot: Failed to parse model response.")
        continue

    if decision_text["action"] == "calculator":
        print("Agent: Using calculator tool...")
        result = calculator(decision["input"])

        final_response = client.models.generate_content(
            model=model_name,
            contents=f"The result of {decision['input']} is {result}, explain the result clearly."
        )

        print("bot:", final_response.text)

    else:
        final_response = client.models.generate_content(
            model=model_name,
            contents=decision['input']
        )

        print("Bot:",final_response.text)