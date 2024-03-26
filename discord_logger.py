import requests
import json
from sms_config import DISCORD_WEBHOOK

def send_logs(message):
    
    response = requests.post(DISCORD_WEBHOOK, data=json.dumps(message), headers={"Content-Type": "application/json"})

    if response.status_code == 204:
        print("Message sent successfully")
    else:
        print("Failed to send message")

def compose_logs(base_url="",data="",job_id="",status=""):
    if status == 'Ongoing...':
        color = 16245426
        emoji = ":hourglass_flowing_sand:"
    else:
        color = 3793585
        emoji = ":white_check_mark:"

    if status == 'Failed':
        message = {
            "content": ":exclamation::exclamation::exclamation:  ALERT :exclamation::exclamation::exclamation: ",
            "embeds": [
                {
                    "title": f"SMS Gateway - ERROR",
                    "color": 16740615,
                    "fields": [
                        {
                            "name": "Unable to ping the Android Server: ",
                            "value": 'Android Server is offline or not reachable. Please check the server and try again or contact the developer.',
                            "inline": False
                        }
                    ]
                }
            ]
        }
        return message

    message = {
            "content": "Announcement!",
            "embeds": [
                {
                    "title": f"SMS Gateway",
                    "color": color,
                    "fields": [
                        {
                            "name": "Environment: ",
                            "value": base_url,
                            "inline": False
                        },
                        {
                            "name": "Job ID ",
                            "value": job_id,
                            "inline": False
                        },
                        {
                            "name": "Total Recipients: ",
                            "value": len(data),
                            "inline": False
                        },
                        {
                            "name": "Status: ",
                            "value": f"{emoji} {status}",
                            "inline": False
                        }
                    ]
                }
            ]
        }
    return message