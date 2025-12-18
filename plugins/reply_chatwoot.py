import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

CHATWOOT_BASE_URL = os.getenv("CHATWOOT_BASE_URL")
CHATWOOT_TOKEN = os.getenv("CHATWOOT_API_TOKEN")

def main():
    payload = json.loads(os.getenv("CHATWOOT_BODY"))

    # filtros básicos
    if payload.get("event") != "message_created":
        return

    if payload.get("message_type") != "incoming":
        return

    if payload.get("private") is True:
        return

    sender_type = payload.get("sender", {}).get("type")
    if sender_type != "contact":
        return

    conversation_id = payload["conversation"]["id"]
    content = payload.get("content", "")

    reply = f"Olá 👋 Recebi sua mensagem: {content}"

    url = f"{CHATWOOT_BASE_URL}/api/v1/accounts/2/conversations/{conversation_id}/messages"

    headers = {
        "api_access_token": CHATWOOT_TOKEN,
        "Content-Type": "application/json",
    }

    body = {
        "content": reply,
        "message_type": "outgoing",
        "private": False,
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    print("Mensagem enviada com sucesso")

if __name__ == "__main__":
    main()
