import time
import requests, sys

url = sys.argv[1].replace('#','&')

requests.get(url)
time.sleep(5)
exit()