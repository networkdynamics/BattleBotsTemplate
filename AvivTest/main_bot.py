import requests
import json

# API endpoint URL
baseUrl = "https://eager-seas-peel.loca.lt"

authenticationToken_for_bot = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIxIiwidGVhbU5hbWUiOiJBdml2VGVzdFRlYW0xIiwiaWF0IjoxNzIyMjg3NjQ0LCJleHAiOjE3MjIzNzQwNDR9.PEz-iXAdLHsddlwhPZqoikE_dARrKazBHcO-AGEgGHs'

# Request body
payload = {
    "num_of_users": 11,
}

try:

    # ask for create users

    response = requests.post(baseUrl + '/api/bot/session/123/createuser', data=payload) 

    # get first subsession

    response2 = requests.post(baseUrl + '/api/bot/session/{session_id}/{sub_session_id}', data=payload) 

    # do some logic

    # InjectSubSession
    
    
    
    # get next subsession

    # ...






    # Make the POST request
    response = requests.post(url, data=payload)



    
    # Check if the request was successful
    response.raise_for_status()
    
    # Print the response
    print("Response status code:", response.status_code)
    print("Response content:", response.json())

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)