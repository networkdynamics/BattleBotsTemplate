from constants import detector_session_id, detect_bot_max_time
import requests
import json
from DetectorTemplate.DetectorCode.detector import Detector
import logging
import signal

logging.basicConfig(
    filename='DetectorTemplate/run.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TimeoutError(Exception):
    """Custom exception for timeout errors."""
    pass

# API endpoint URL
base_url = "http://localhost:3000"

authentication_token_for_detector = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiI0IiwidGVhbU5hbWUiOiJFbWlsaWUgRGV0ZWN0b3IiLCJpYXQiOjE3MjM4NTUyODksImV4cCI6MTcyMzk0MTY4OX0.lTzqaLW3tcLO15_CGsyNA-SWYhl1UDlRGwJozbyJU-A'

headers = {'Authorization': 'bearer ' + authentication_token_for_detector, 'Content-Type': 'application/json' }

def handler(signum, frame):
    raise TimeoutError("Timeout Error:")

logging.info(f"START SESSION {detector_session_id}")
try:
    detector = Detector()
    # ask for Session Info
    session_dataset = requests.get(base_url + '/api/detector/session/' + str(detector_session_id), headers=headers) 
    
    session_dataset.raise_for_status()

    logging.info(f"Get Session response status code: {session_dataset.status_code}")
    print("Get Session response status code:", session_dataset.status_code)
    print("Get Session response content:", session_dataset.json())

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(detect_bot_max_time)
    try:
        detections_submission = detector.detect_bot(session_dataset.json())
    except TimeoutError as exc:
        logging.error(f"{exc} The code took more than one hour to run. Continue with an empty submission.")
        print(f"{exc} The code took more than one hour to run. Continue with an empty submission.")
        detections_submission = json.dumps({"users": []})

    signal.alarm(0)

    submission_confirmation = requests.post(base_url + '/api/detector/session/' + str(detector_session_id), headers=headers, data=detections_submission) 

    
    # Check if the request was successful
    submission_confirmation.raise_for_status()
    
    # Print the response
    logging.info(f"Detection Submission repsonse status code: {submission_confirmation.status_code}")
    print("Detection Submission repsonse status code:", submission_confirmation.status_code)
    print("Detection Submission response content:", json.dumps(submission_confirmation.json(), indent=4))

    logging.info(f"END SESSION {detector_session_id}")

except requests.exceptions.RequestException as e:
    logging.error(f"An error occurred: {e}")
    print("An error occurred:", e)