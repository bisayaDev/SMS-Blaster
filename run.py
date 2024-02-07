import os
import time
from sms_config import *
os.system(f"start /B start cmd.exe @cmd /k \"venv\\Scripts\\activate & python main.py\"")
time.sleep(2)
os.system(f"start /B start cmd.exe @cmd /k \"deactivate & ngrok http --domain={NGROK_DOMAIN} {BROADCAST_PORT}\"")