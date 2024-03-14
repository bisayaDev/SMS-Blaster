import requests
import sms_config

def get_token(url):
    url = f"https://{url}.ecitizenph.com/api/tokens/create"
    params = dict(
        email=sms_config.TOKEN_USERNAME,
        password=sms_config.TOKEN_PASSWORD,
        token_name="bearer_token",
    )

    response = requests.post(url, params)
    token = response.json()['token']
    
    headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'text/plain'
        }

    return headers
