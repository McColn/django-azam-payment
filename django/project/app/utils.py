import requests

def get_azampay_token():
    url = "https://authenticator-sandbox.azampay.co.tz/AppRegistration/GenerateToken"
    headers = {"Content-Type": "application/json"}
    payload = {
        "appName": "McColn",
        "clientId": "xxxxx",
        "clientSecret": "xxxxxxxx"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        access_token = response.json().get("data", {}).get("accessToken")
        print("✅ Token Generated Successfully:", access_token)
        return access_token

    return None
