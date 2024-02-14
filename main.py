import os
from starlette.responses import HTMLResponse
from fastapi import FastAPI, BackgroundTasks
import requests, json
from dotenv import load_dotenv
import asyncio
from html_design import index_view
from sms_config import *
from tcping import Ping
from discord_logger import send_logs

load_dotenv()
app = FastAPI()



async def background_task(duration: int, data: list):
    print(f"Background task started: {duration} seconds interval")

    for item in data:
        num = fix_cp_numbers(item['phone_number'])
        if not num:
            continue
        SendSms(item['text'],num,item['id'],item['url'])
        await asyncio.sleep(duration)

    print(f"Background task completed: {duration * len(data)} seconds")

async def bg_tasker(background_tasks: BackgroundTasks, data: list):
    background_tasks.add_task(background_task, 5, data)

@app.get("/send_bulk_sms/")
async def root(base_url: str,job_id: int, background_tasks: BackgroundTasks = None):
    data = get_jobs(job_id,base_url)
    if ping_server_api():
        send_logs(compose_logs(base_url,data,job_id,'Ongoing...'))
        response_data = await bg_tasker(background_tasks, data)
        return {"success":"Background task started."}
    else:
        return {"error":"Android SMS Gateway is offline."}

def get_jobs(id,base_url):
    if base_url == "local":
        url = "localhost"
    else:
        url = f"https://{base_url}.ecitizenph.com"

    try:
        result = requests.get(f'{url}/api/sms/get-recipients/{id}').json()
    except Exception as e:
        result = []
        print(e)

    if result:
        for i in result:
            i['url'] = url
    return result

@app.get("/", response_class=HTMLResponse)
def index():
    return index_view()


def SendSms(message,send_to,id,base_url):
  url = f"http://{SMS_APP_URL}:{SMS_APP_PORT}/services/api/messaging/"
  params = {
    'to': send_to,
    'message': message
  }
  res = requests.post(url, params=params)
  update_sent_msg_status(base_url,id)

def trim_data(data):
    json_data = json.loads(data)
    return json_data

def update_sent_msg_status(base_url,id):
    try:
        if base_url == 'local':
            url = f'https://localhost/api/sms/{id}/update-sent/'
        else:
            url = f'{base_url}/api/sms/{id}/update-sent/'
        headers = {'Authorization': API_KEY}
        requests.put(url, headers=headers)
    except:
        print(f"Database update error. id = {id}")

def ping_server_api():
    ping = Ping(SMS_APP_URL,SMS_APP_PORT,30)
    try:
        ping.ping(1)
        return True
    except:
        return False

def fix_cp_numbers(num):
    if num.startswith('09') and len(num) == 11:
        return num
    elif num.startswith('+639') and len(num) == 13:
        return num
    elif num.startswith('639') and len(num) == 12:
        return num
    elif num.startswith('9') and len(num) == 10:
        return f"0{num}"

def compose_logs(base_url,data,job_id,status):
    if base_url == 'staging':
        env = "STAGING"
    else:
        env = "PRODUCTION"


    message = f"""
Env: {env}
Site: {base_url}
# of Recepients: {len(data)}
Status: {status}
    """
    return message

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=BROADCAST_PORT)
