import requests
import json

# API endpoint URL
url = "https://eager-seas-peel.loca.lt/api/bot/session/temp"

# Request body
payload = {
    "num_of_users": 10,
}

try:
    # Make the POST request
    response = requests.post(url, data=payload)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Print the response
    print("Response status code:", response.status_code)
    print("Response content:", response.json())

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)