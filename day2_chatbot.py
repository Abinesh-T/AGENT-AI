from get_client import client

chat_history = []

while True:
    user_input = input("you: ")

    if user_input == "quit":
        break

    chat_history.append({
        "role": "user",
        "parts":[{"text": user_input}]
    })

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=chat_history
    )

    bot_reply = response.text
    print("Bot:", bot_reply)

    chat_history.append({
        "role": "model",
        "parts":[{"text": bot_reply}]
    })