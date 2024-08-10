import requests
import json
import detector_logic

# API endpoint URL
baseUrl = "http://54.88.122.105:3000"

authenticationToken_for_detector = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIyIiwidGVhbU5hbWUiOiJBdml2RGV0ZWN0b3IxIiwiaWF0IjoxNzIyMjgzNjIwLCJleHAiOjE3MjIzNzAwMjB9.rD6FOrD-h22_1l5CQQqSY7pMOj0qZCOeFaXyy48Ev1A'

headers = {'Authorization': 'bearer ' + authenticationToken_for_detector, 'Content-Type': 'application/json' }

sessionId = 4

try:

    # ask for Session Info
    sessionResponse = requests.get(baseUrl + '/api/detector/session/' + str(sessionId), headers=headers) 
    
    sessionResponse.raise_for_status()

    print("Response status code:", sessionResponse.status_code)
    print("Response content:", sessionResponse.json())

    detections = detector_logic.calculateDetections(sessionResponse.json())

    detection = requests.post(baseUrl + '/api/detector/session/' + str(sessionId), headers=headers, data=detections) 

    
    # Check if the request was successful
    detection.raise_for_status()
    
    # Print the response
    print("Response status code:", detection.status_code)
    print("Response content:", detection.json())

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)