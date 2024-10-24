import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from DetectorTemplate.DetectorCode.detector import Detector
import logging
import signal
from pydantic import ValidationError
from teams_classes import DetectionMark
from api_requests import get_session_data, submit_detection
import json

session_id = int(os.getenv('SESSION_ID'))
code_max_time = int(os.getenv('MAX_TIME'))

logging.basicConfig(
    filename='run.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TimeoutError(Exception):
    """Custom exception for timeout errors."""
    pass

class MarkingMissingUsers(Exception):
    """Custom exception for marking missing users errors."""
    pass

class MultipleDetectionForUser(Exception):
    """Custom exception for multiple detection for user errors."""
    pass

def handler(signum, frame):
    raise TimeoutError("Timeout Error:")

logging.info(f"START SESSION {session_id}")
try:
    detector = Detector()
    # ask for Session Info
    get_session_response, session_dataset = get_session_data()

    all_id_set = set()
    for user in session_dataset.users:
        all_id_set.add(user['id'])
    
    get_session_response.raise_for_status()

    logging.info(f"Get Session response status code: {get_session_response.status_code}")
    print("Get Session response status code:", get_session_response.status_code)
    #print("Get Session response content:", session_dataset.json())

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(code_max_time)
    try:
        marked_account = detector.detect_bot(session_dataset)
        marked_id_set = set()
        for account in marked_account:
            marked_id_set.add(account.user_id)

        if len(marked_account) == 0: # Empty submission
            detections_submission = []
        elif not len(marked_account) == len(marked_id_set):
            raise MultipleDetectionForUser("Every user need to have one DetectionMark only. At least one user have more then 1 DetectionMark.")
        elif not all_id_set == marked_id_set:
            raise MarkingMissingUsers("Your submission is not giving a results for every users of the dataset. Make sure to make a DetectionMark for every user.")
        elif not isinstance(marked_account[0], DetectionMark): # If the teams don't return a list of DetectionMark instance/object.
            raise TypeError(f"The elements of the list should be DetectionMark instance not {type(marked_account[0])}. Make sure to return a list[DetectionMark].")
        else:
            detections_submission = [user.to_dict() for user in marked_account]
    except TimeoutError as exc:
        logging.error(f"{exc} The code took more than one hour to run. Continue with an empty submission.")
        print(f"{exc} The code took more than one hour to run. Continue with an empty submission.")
        detections_submission = []

    submission_confirmation = submit_detection(detections_submission) 
    
    # Check if the request was successful
    submission_confirmation.raise_for_status()
    
    # Print the response
    logging.info(f"Detection Submission repsonse status code: {submission_confirmation.status_code}")
    print("Detection Submission repsonse status code:", submission_confirmation.status_code)
    #print("Detection Submission response content:", json.dumps(submission_confirmation.json(), indent=4))

    signal.alarm(0)
    logging.info(f"END SESSION {session_id}")

except (requests.exceptions.RequestException, ValidationError, TypeError, MarkingMissingUsers, MultipleDetectionForUser) as exc:
    if isinstance(exc, requests.exceptions.RequestException):
        logging.error(f"An error occurred: {exc}")
        print("An error occurred:", exc)
    elif isinstance(exc, ValidationError):
        if exc.errors()[0]['type'] == 'int_from_float':
            logging.error(f"DetectionMark Object Error: The confidence should be an int between 0 (definitely not a bot) and 100 (definitely a bot). Error Description {exc.errors()}.")
            print(f"DetectionMark Object Error: The confidence should be an int between 0 (definitely not a bot) and 100 (definitely a bot). Error Description {exc.errors()}.")
        else:
            logging.error(f"DetectionMark Object Error: Error Description {exc.errors()}. Make sure you create your instance correctly.")
            print(f"DetectionMark Object Error: Error Description {exc.errors()}. Make sure you create your instance correctly.")
    elif isinstance(exc, (TypeError, MarkingMissingUsers, MultipleDetectionForUser)):
        logging.error(exc)
        print(exc)