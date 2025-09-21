# secure_listener.py

import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
from agents.agents import agent_handler
# --- 1. LOAD SECURE CREDENTIALS ---
# This line looks for a .env file in the same directory and loads the variables.
load_dotenv()

# Get the credentials from the environment. os.getenv() safely reads the variables.
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION_NAME = os.getenv('SESSION_NAME')

# --- 2. THE TELEGRAM CLIENT AND EVENT LISTENER ---
# The script uses the loaded credentials to connect to Telegram.
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    """This function runs automatically when a new private message is received."""
    sender = await event.get_sender()
    sender_username = sender.username if sender.username else "N/A"
    message_content = event.message.message
    content += message_content
    if len(content) > 300:
        result = agent_handler(content)
        print("Misinformation checker results:", result)
        content = ""

    # --- THIS IS YOUR "NOTIFICATION" IN THE SERVER TERMINAL ---
    # It prints the message details in a clean format directly to your screen.
    print("-----------------------------------------")
    print(f"📩 NEW MESSAGE RECEIVED")
    print(f"   - From: {sender.first_name} (@{sender_username})")
    print(f"   - Message: \"{message_content}\"")
    print("-----------------------------------------")
    print() # Adds a blank line for better readability

# --- 3. START THE SCRIPT ---
# Start the client by connecting to Telegram.
client.start()

# Print a startup message so you know the script is active.
print("✅ Script is running and securely listening for new messages...")

# This line makes the script wait here forever, keeping it alive to
# receive new messages. You can stop it by pressing Ctrl+C.
client.run_until_disconnected()
"""
import requests

FCM_SERVER_KEY = "YOUR_FCM_SERVER_KEY"

def push_to_flutter(title, body, token):
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {
        "Authorization": f"key={FCM_SERVER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": token,
        "notification": {
            "title": title,
            "body": body
        },
        "data": {"extra": "value"}  # optional
    }
    requests.post(url, headers=headers, json=payload)



"""
