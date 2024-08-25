from fastapi import FastAPI, HTTPException, Request
import requests

app = FastAPI()

SLACK_BOT_TOKEN = "<token>"


@app.post("/send_message")
async def send_message(request: Request):
    data = await request.json()
    message = data.get("message")
    message_link = data.get("link")
    email = data.get("email")

    if not message or not email:
        raise HTTPException(status_code=400, detail="Message and email are required")

    # Get Slack user ID based on email
    user_id = get_slack_user_id_by_email(email)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    # Send DM to Slack user
    send_slack_dm(user_id, message, message_link)

    return {"status": "success"}

def get_slack_user_id_by_email(email: str):
    url = "https://slack.com/api/users.lookupByEmail"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    params = {"email": email}

    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    if response_data.get("ok"):
        return response_data["user"]["id"]
    return None

def send_slack_dm(user_id: str, message: str, message_link: str):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    data = {"channel": user_id, "text": message, "message_link": message_link}

    response = requests.post(url, headers=headers, json=data)
    return response.json()