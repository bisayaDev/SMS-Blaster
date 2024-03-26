import os
from ip_port_scanner import *
from dotenv import load_dotenv
load_dotenv()

def index_view():
    stats = ping_server_api()
    view = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <title>eCitizenPH</title>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
          <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
        </head>
        <body>
        <div class="row">
            <div class="col-12 text-center"><h1>eCitizenPH - Android SMS Blaster Status</h1></div>
        </div>
        <div class="row text-center">
            <span>Android Server Status: <b>{stats['status']}</b></span>
            <span>Android Server Count: <b>{stats['count']}</b></span>
            <span>Android Servers: <b>{stats['servers']}</b></span>
        </div>
        </body>
        </html>
    """
    return view

def ping_server_api():
    phones = get_all_running_device()

    if phones:
        status = "✅ ONLINE ✅"
    else:
        status = "❌ OFFLINE ❌"


    response = {
        'status': status,
        'count' : len(phones),
        'servers': phones
    }

    return response
