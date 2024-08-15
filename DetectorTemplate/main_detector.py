import requests
import json
from DetectorCode.detector_logic import Detector
import signal

# API endpoint URL
baseUrl = "http://localhost:3000"

authenticationToken_for_detector = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiI0IiwidGVhbU5hbWUiOiJFbWlsaWUgRGV0ZWN0b3IiLCJpYXQiOjE3MjM2ODMwOTYsImV4cCI6MTcyMzc2OTQ5Nn0.aH4YkdfIfWC7CbseVkjN88icUKcM6hm_0gTZ4ggt3kE'

headers = {'Authorization': 'bearer ' + authenticationToken_for_detector, 'Content-Type': 'application/json' }

sessionId = 4

def handler(signum, frame):
    raise Exception("Timeout")

try:

    # ask for Session Info
    sessionResponse = requests.get(baseUrl + '/api/detector/session/' + str(sessionId), headers=headers) 
    
    sessionResponse.raise_for_status()

    print("Response status code:", sessionResponse.status_code)
    print("Response content:", sessionResponse.json())

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(3601)
    try:
        detections = Detector.calculateDetections(sessionResponse.json())
    except Exception as exc:
        print(exc)
        print("Timeout: The code took more than one hour to run. Continue with an empty submission.")
        detections = json.dumps({"users": []})

    signal.alarm(0)

    detection = requests.post(baseUrl + '/api/detector/session/' + str(sessionId), headers=headers, data=detections) 

    
    # Check if the request was successful
    detection.raise_for_status()
    
    # Print the response
    print("Response status code:", detection.status_code)
    print("Response content:", json.dumps(detection.json(), indent=4))

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)