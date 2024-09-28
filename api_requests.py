import os
import requests
from constants import bot_session_id, detector_session_id
import json

# Environment Variables
base_url = os.getenv('BASE_URL')
authentication_token = os.getenv('AUTH_TOKEN')

header = {'Authorization': 'bearer ' + authentication_token, 'Content-Type': 'application/json'}

#BOT SECTION
class SessionInfo:
    def __init__(self, data):
        self.session_id = data["session_id"]
        self.lang = data["lang"]
        self.metadata = data["metadata"]
        self.influence_target = data["influence_target"]
        self.start_time = data["start_time"]
        self.end_time = data["end_time"]
        self.sub_sessions_info = data["sub_sessions_info"]
        self.sub_sessions_id = [sub_session["sub_session_id"] for sub_session in data["sub_sessions_info"]]
        self.users = data["users"]
        self.usernames = set([user["username"] for user in data["users"]])

class SubSessionDataset:
    def __init__(self, data):
        self.session_id = data["session_id"]
        self.sub_session_id = data["sub_session_id"]
        self.posts = data["posts"]
        self.users = data["users"]

def get_session_info():
    response = requests.get(base_url + '/bot/session/' + str(bot_session_id) + '/info', headers=header)
    if response.status_code >= 400:
        return response, []
    else:
        return response, SessionInfo(response.json())
    
def create_user_id(number_users):
    response = requests.post(base_url + '/bot/session/' + str(bot_session_id) + '/createuser', headers=header, data=json.dumps({"num_of_users": number_users}))
    users_id_list = []
    for user in response.json()['users']:
        users_id_list.append(user['id'])

    return response, users_id_list
    
def get_sub_session(sub_session):
    response = requests.get(base_url + '/bot/session/' + str(bot_session_id) + '/' + str(sub_session), headers=header)
    if response.status_code >= 400:
        return response, []
    else:
        return response, SubSessionDataset(response.json())
    
def submit_injection(sub_session, posts_submission, users_submission):
    print(json.dumps({"posts": posts_submission, "users": users_submission}, indent=4))
    return requests.post(base_url + '/bot/session/' + str(bot_session_id) + '/' + str(sub_session), headers=header, data=json.dumps({"posts": posts_submission, "users": users_submission}))

# DETECTOR SECTION
class SessionDataset:
    def __init__(self, data):
        self.session_id = data["id"]
        self.lang = data["lang"]
        self.metadata = data["metadata"]
        self.posts = data["posts"]
        self.users = data["users"]

def get_session_data():
    response = requests.get(base_url + '/detector/session/' + str(detector_session_id), headers=header)
    if response.status_code >= 400:
        return response, []
    else:
        return response, SessionDataset(response.json())
    
def submit_detection(detections_submission):
    return requests.post(base_url + '/detector/session/' + str(detector_session_id), headers=header, data=json.dumps({"users": detections_submission}))