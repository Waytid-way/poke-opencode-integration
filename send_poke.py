import requests
import json
import os
import sys

def send_poke_notification(message, api_key):
    """
    Sends a POST request to Poke's inbound webhook API.
    """
    url = "https://poke.com/api/v1/inbound-sms/webhook"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": message
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Successfully sent message to Poke: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Poke: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Example usage: python send_poke.py "Hello from Opencode!"
    if len(sys.argv) < 2:
        print("Usage: python send_poke.py <message>")
        sys.exit(1)
    
    msg = sys.argv[1]
    # It is recommended to store your API key in an environment variable
    token = os.getenv("POKE_API_KEY")
    
    if not token:
        print("Error: POKE_API_KEY environment variable not set.")
        sys.exit(1)
        
    send_poke_notification(msg, token)
