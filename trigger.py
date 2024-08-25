import requests
import json

# Define the data to be sent in the POST request
data = {
    "message": "Hello, this is a test message!",
    "email": "mrabkaraliparambil@gmail.com",
    "message_link": "mr-k-ab.github.io"
}


url = "http://127.0.0.1:8000/send_message"

# Make the POST request to the specified URL
response = requests.post(
    url,
    headers={"Content-Type": "application/json"},
    data=json.dumps(data)
)

# Handle the response
if response.ok:
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
