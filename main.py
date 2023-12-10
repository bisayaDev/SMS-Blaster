import os
from fastapi import FastAPI, Query, BackgroundTasks
from typing import List, Annotated
import requests, json
from dotenv import load_dotenv
import asyncio
from html_design import view
from sms_config import API_KEY

load_dotenv()
app = FastAPI()



async def background_task(duration: int, data: list):
    print(f"Background task started: {duration} seconds")
    for item in data:
        SendSms(item['text'],item['phone_number'],item['id'])
        await asyncio.sleep(duration)

    print(f"Background task completed: {duration} seconds")

async def bg_tasker(background_tasks: BackgroundTasks, data: list):
    background_tasks.add_task(background_task, 10, data)
    return {"message": "Hello, World!"}

@app.get("/send_bulk_sms/")
async def root(data: Annotated[list, Query()] = [], background_tasks: BackgroundTasks = None):
    trimmed_data = trim_data(data[0])
    # Correct way to call bg_tasker and await its completion
    response_data = await bg_tasker(background_tasks, trimmed_data)
    return '{"success":"Background task started"}'

@app.get("/")
async def index():
    return view


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
        pinged = ping.ping(1)
        return True
    except:
        return False