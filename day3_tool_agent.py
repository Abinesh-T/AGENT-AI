from get_client import client
import re

model_name = "models/gemini-2.5-flash"

def calculator(expression: str):
    try:
        return str(eval(expression))
    except Exception:
        return "invalid math expression."

print("Tool Agent (type 'exit to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break


    if re.search(r"[\d+\-*/()]",user_input):
        print("Agent:using calculator tool...")
        result = calculator(user_input)
        print("Bot:",result)
    else:
        response = client.models.generate_content(
            model=model_name,
            contents=user_input
        )

        print("Bot:",response.text)
