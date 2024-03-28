import os, sys
from starlette.responses import HTMLResponse
from fastapi import FastAPI, BackgroundTasks
import requests, json
from dotenv import load_dotenv
import asyncio
from html_design import index_view
from sms_config import *
from discord_logger import send_logs, compose_logs
from tokenizer import get_token
from ip_port_scanner import get_all_running_device
from helper import *

load_dotenv()
app = FastAPI()
headers = {}
job_list = []
is_running = False


async def background_task(duration: int, data: list):
    print(f"Background task started: {duration} seconds interval")
    for item in data:
        num = fix_cp_numbers(item['phone_number'])
        if not num:
            continue
        SendSms(item['text'], num, item['id'], item['url'])
        await asyncio.sleep(duration)

    send_logs(compose_logs(data[0]['base_url'], data, data[0]['job_id'], 'Completed!!'))
    print(f"Background task completed: {duration * len(data)} seconds")


async def background_multitask(duration: int, data: list, active_phones: list):
    global job_list, is_running
    print(f"Background Multitask started for Job ID: {data[0][0]['job_id']}")
    is_running = True
    max_length = max(len(group) for group in data)

    for i in range(max_length):
        for j, group in enumerate(data):
            if i < len(group):
                num = fix_cp_numbers(group[i]['phone_number'])
                if not num:
                    print(f"invalid phone: {group[i]['phone_number']}")
                    continue
                arraySend(
                    phone=active_phones[j % len(active_phones)],
                    send_to=num,
                    message=group[i]['text'],
                    base_url=group[i]['url'],
                    record_id=group[i]['id'],
                )
        await asyncio.sleep(duration)

    is_running = False
    check_pending_job(data[0][0]['job_id'])

    send_logs(compose_logs(data[0][0]['base_url'], data, data[0][0]['job_id'], 'Completed!!'))
    print(f"Job ID: {data[0][0]['job_id']} is done.")

async def bg_tasker(background_tasks: BackgroundTasks, data: list):
    background_tasks.add_task(background_task, 5, data)


async def bg_tasker_multi_phone(background_tasks: BackgroundTasks, data: list, active_phones: list):
    background_tasks.add_task(background_multitask, 5, data, active_phones)


@app.get("/send_bulk_sms/")
async def root(base_url: str, job_id: int, background_tasks: BackgroundTasks = None):
    global headers, is_running
    headers = get_token(base_url)
    data = get_jobs(job_id,base_url)
    active_phones = get_all_running_device()

    job = {"base_url": base_url, "job_id": job_id}
    job_list.append(job)

    if is_running:
        print(f'Added new job to the queue. Job ID: {job_id}')
        return {"status": "pending", "message": "There's an in-progress sms blast. Your Sms blast is in queue."}

    if len(active_phones) > 0:
        grouped_data = group_data_by(data, len(active_phones))
        send_logs(compose_logs(base_url, data, job_id, 'Ongoing...'))

        await bg_tasker_multi_phone(background_tasks, grouped_data, active_phones)
    else:
        return {"status": "error", "message": "There's no active SMS Gateway device."}

    return {"status": "success", "message": "Background task started."}


def get_jobs(id, base_url):
    global headers
    if base_url == "local":
        url = "localhost"
    else:
        url = f"https://{base_url}.ecitizenph.com"

    try:
        result = requests.get(f'{url}/api/sms/get-recipients/{id}', headers=headers).json()
    except Exception as e:
        result = []
        print(e)

    if result:
        for i in result:
            i['url'] = url
            i['job_id'] = id
            i['base_url'] = base_url
    return result

@app.get("/", response_class=HTMLResponse)
def index():
    return index_view()


def SendSms(message, send_to, id, base_url):
    global headers
    url = f"http://{SMS_APP_URL}:{SMS_APP_PORT}/services/api/messaging/"
    params = {
        'to': send_to,
        'message': message
    }
    res = requests.post(url, params=params, headers=headers)
    update_sent_msg_status(base_url, id)


def arraySend(phone, send_to, message, base_url, record_id):
    global headers
    url = f"http://{phone}:{SMS_APP_PORT}/services/api/messaging/"
    params = {
        'to': send_to,
        'message': message
    }

    try:
        requests.post(url, params=params, headers=headers)
    except:
        print(f"There's problem sending the message. Record ID: {record_id}")

    update_sent_msg_status(base_url, record_id)


def update_sent_msg_status(base_url, id):
    global headers
    try:
        if base_url == 'local':
            url = f'https://localhost/api/sms/{id}/update-sent/'
        else:
            url = f'{base_url}/api/sms/{id}/update-sent/'
        requests.put(url, headers=headers)
    except:
        print(f"Database update error. id = {id}")

@app.get("/status")
def get_all_active_phone():
    all_device = get_all_running_device()
    if all_device:
        status = 'online'
    else:
        status = 'offline'

    response = {
        'status' : status,
        'Server Count': len(all_device),
        'Servers': all_device,
    }

    return response

def check_pending_job(job_id):
    global job_list

    job_list = [item for item in job_list if item['job_id'] != job_id]

    if job_list:
        url = f"https://{NGROK_DOMAIN}/send_bulk_sms?base_url={job_list[0]['base_url']}#job_id={job_list[0]['job_id']}"
        print(f"REQUESTING : {url}")
        try:
            os.system(f"start /B start cmd.exe @cmd /k \"python job_request.py {url}\"")
        except:
            print(f"Error re-running the job. Job ID: {job_list[0][job_id]}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=BROADCAST_PORT)
