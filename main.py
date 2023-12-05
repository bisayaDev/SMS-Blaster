import os
import time

from fastapi import FastAPI, Query
from typing import List, Annotated
import requests, json
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/send_bulk_sms/")
async def root(data: Annotated[list, Query()] = []):
    trimmed_data = trim_data(data)
    for item in trimmed_data:
        res = SendSms(item['message'],item['send_to'])
        if res.status_code == 200:
            update_sent_msg_status(item['id'])
    return "Success"

def SendSms(message,send_to):
  url = "http://" + os.getenv('APP_URL') + ":" + os.getenv('APP_PORT') + "/services/api/messaging/"
  params = {
    'to': send_to,
    'message': message
  }
  res = requests.post(url, params=params)
  return res

def trim_data(data):
    data = data
    return data

def update_sent_msg_status(id):
    time.sleep(10)
    return "Updated"