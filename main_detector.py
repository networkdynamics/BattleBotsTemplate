import requests
import json
import detector

# API endpoint URL
baseUrl = "http://localhost:3000"

authenticationToken_for_detector = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIyIiwidGVhbU5hbWUiOiJBdml2RGV0ZWN0b3IxIiwiaWF0IjoxNzIyMjgzNjIwLCJleHAiOjE3MjIzNzAwMjB9.rD6FOrD-h22_1l5CQQqSY7pMOj0qZCOeFaXyy48Ev1A'

# Request body
payload = {
    "num_of_users": 4
}

headers = {'Authorization': 'bearer ' + authenticationToken_for_detector, 'Content-Type': 'application/json' }

sessionId = 1

try:

    # ask for Session Info
    sessionResponse = requests.get(baseUrl + '/api/detector/session/' + str(sessionId), headers=headers)

    # Check if the request was successful
    sessionResponse.raise_for_status()

    # Print the response
    print("Response status code:", sessionResponse.status_code)
    print("Response content:", sessionResponse.json())
    
    
    detections = detector.calculateDetections(sessionResponse.json())
    print('detections ' + str(detections))
    detection = requests.post(baseUrl + '/api/detector/session/' + str(sessionId), headers=headers, data=detections) 

    
    # Check if the request was successful
    detection.raise_for_status()
    
    # Print the response
    print("Response status code:", detection.status_code)
    print("Response content:", detection.json())

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)