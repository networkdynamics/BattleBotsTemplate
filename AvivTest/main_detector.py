import requests
import json

# API endpoint URL
baseUrl = "https://funny-buses-agree.loca.lt"

authenticationToken_for_detector = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIyIiwidGVhbU5hbWUiOiJBdml2RGV0ZWN0b3IxIiwiaWF0IjoxNzIyMjgzNjIwLCJleHAiOjE3MjIzNzAwMjB9.rD6FOrD-h22_1l5CQQqSY7pMOj0qZCOeFaXyy48Ev1A'

# Request body
payload = {
    "num_of_users": 11,
}

headers = {'Authorization': 'bearer ' + authenticationToken_for_detector }

sessionId = 1

try:

    # ask for Session Info

    response = requests.get(baseUrl + '/api/detector/session/1', headers=headers, data=payload) 
    print('asdf' + str(response))

    # do some logic

    # Detect Session

    



    
    # Check if the request was successful
    response.raise_for_status()
    
    # Print the response
    print("Response status code:", response.status_code)
    print("Response content:", response.json())

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)