# slack_labelling_tool_alert_app
By V P MIS AB


## Step by step instructions

### 1. **Create a Slack App:**
   - Go to the [Slack API](https://api.slack.com/apps) page and create a new app.
   - Choose "From scratch" and give your app a name and workspace.
   - Under "OAuth & Permissions," add the `chat:write` and `users:read` scopes.
   - Install the app to your workspace and note down the "Bot User OAuth Token."

### 2. **Create a Webhook Endpoint:**
   You'll need to create an endpoint on your website that can receive HTTP POST requests containing the message and email ID. You can use FastAPI, Flask, or any other web framework. Here's an example using FastAPI:

   ```python
   from fastapi import FastAPI, HTTPException, Request
   import requests

   app = FastAPI()
   SLACK_BOT_TOKEN = "xoxb-your-slack-bot-token"

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
       data = {"channel": user_id, "text": message}

       response = requests.post(url, headers=headers, json=data)
       return response.json()
   ```

   This FastAPI app listens for POST requests at the `/send_message` endpoint, looks up the Slack user by email, and sends a DM with the provided message.

### 3. **Deploy the Webhook Endpoint:**
   Deploy this FastAPI app on a server or cloud service where it can be publicly accessible.

### 4. **Trigger the Webhook from Your Website:**
   From your website, make a POST request to the deployed webhook endpoint with the message and email ID.

   Example using JavaScript:

   ```javascript
   const message = "Hello, this is a test message!";
   const email = "user@example.com";

   fetch("https://your-domain.com/send_message", {
       method: "POST",
       headers: {
           "Content-Type": "application/json"
       },
       body: JSON.stringify({ message: message, email: email })
   })
   .then(response => response.json())
   .then(data => console.log(data))
   .catch(error => console.error('Error:', error));
   ```

### 5. **Test the Integration:**
   Once everything is set up, test the integration by sending a message from your website and ensuring that the Slack user receives a DM.

This should give you a solid foundation for building a Slack bot that sends DMs triggered by a webhook. Let me know if you need any further customization!
