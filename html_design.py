import os
from tcping import Ping
from dotenv import load_dotenv
load_dotenv()

def index_view():
    view = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <title>Bootstrap Example</title>
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
            <span>ANDROID GATEWAY STATUS: {ping_server_api()}</span>
        </div>
        </body>
        </html>
    """
    return view

def ping_server_api():
    ping = Ping(os.getenv('APP_URL'),os.getenv('APP_PORT'),60)
    try:
        pinged = ping.ping(1)
        return "✅"
    except:
        return "❌"
