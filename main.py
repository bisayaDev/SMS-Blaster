import os
from starlette.responses import HTMLResponse
from fastapi import FastAPI, BackgroundTasks
import requests, json
from dotenv import load_dotenv
import asyncio
from html_design import index_view
from sms_config import API_KEY
from tcping import Ping

load_dotenv()
app = FastAPI()



async def background_task(duration: int, data: list):
    print(f"Background task started: {duration} seconds")

    for item in data:
        SendSms(item['text'],item['phone_number'],item['id'])
        await asyncio.sleep(duration)

    print(f"Background task completed: {duration} seconds")

async def bg_tasker(background_tasks: BackgroundTasks, data: list):
    background_tasks.add_task(background_task, 5, data)

@app.get("/send_bulk_sms/")
async def root(base_url: str,job_id: int, background_tasks: BackgroundTasks = None):
    data = get_jobs(job_id,base_url)
    if ping_server_api():
        response_data = await bg_tasker(background_tasks, data)
        return {"success":"Background task started."}
    else:
        return {"error":"Android SMS Gateway is offline."}

def get_jobs(id,url):
    location_url = f"https://{url}.ecitizenph.com/api"
    try:
        result = requests.get(f'{location_url}/sms/get-recipients/').json()
    except Exception as e:
        result = []
        print(e)
    return result

@app.get("/", response_class=HTMLResponse)
def index():
    return index_view()


def SendSms(message,send_to,id):
  url = "http://" + os.getenv('APP_URL') + ":" + os.getenv('APP_PORT') + "/services/api/messaging/"
  params = {
    'to': send_to,
    'message': message
  }
  res = requests.post(url, params=params)
  update_sent_msg_status("staging.ecitizenph.com/api",id)
def trim_data(data):
    json_data = json.loads(data)
    return json_data

def update_sent_msg_status(base_url,id):
    try:
        url = f'https://{base_url}/sms/{id}/update-sent/'
        headers = {'Authorization': API_KEY}
        requests.put(url, headers=headers)
    except:
        print("Database update error.")

def ping_server_api():
    ping = Ping(os.getenv('APP_URL'),os.getenv('APP_PORT'),60)
    try:
        ping.ping(1)
        return True
    except:
        return False

