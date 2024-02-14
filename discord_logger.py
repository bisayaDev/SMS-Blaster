import requests
import json
from sms_config import DISCORD_WEBHOOK

def send_logs(message):
    
    response = requests.post(DISCORD_WEBHOOK, data=json.dumps(message), headers={"Content-Type": "application/json"})

    if response.status_code == 204:
        print("Message sent successfully")
    else:
        print("Failed to send message")