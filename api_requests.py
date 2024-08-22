import requests
from constants import bot_session_id, detector_session_id
import json

# Environment Variables
base_url = 'http://localhost:3000'
# Bot authentication_token
authentication_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIxIiwidGVhbU5hbWUiOiJCb3QxIiwiaWF0IjoxNzI0MzU3ODI4LCJleHAiOjE3MjQ0NDQyMjh9.TPu0XREGcAPJNt1Ud0CIH53vtAfa90r9e_7nSKHF4qQ'
# Detector authentication_token
#authentication_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIzIiwidGVhbU5hbWUiOiJEZXRlY3RvcjEiLCJpYXQiOjE3MjQzNTY5MTMsImV4cCI6MTcyNDQ0MzMxM30.RkzdAZCyoTW77fLn7tmDkM6wHd8a-7Ok-UFOicIcrt4'
header = {'Authorization': 'bearer ' + authentication_token, 'Content-Type': 'application/json'}

#BOT SECTION
class SessionInfo:
    def __init__(self, data):
        self.session_id = data["session_id"]
        self.metadata = data["metadata"]
        self.sub_sessions_id = data["sub_sessions_id"]
        self.influence_target = data["influence_target"]
        self.users = data["users"]

class SubSessionDataset:
    def __init__(self, data):
        self.sub_session_id = data["sub_session_id"]
        self.metadata = data["metadata"]
        self.posts = data["posts"]
        #self.users = data["users"]

def get_session_info():
    response = requests.get(base_url + '/api/bot/session/' + str(bot_session_id) + '/info', headers=header)
    print(response.text)
    print(response.content)
    return response, SessionInfo(response.json())
    
def create_user_id(number_users):
    response = requests.post(base_url + '/api/bot/session/' + str(bot_session_id) + '/createuser', headers=header, data=json.dumps({"num_of_users": number_users}))
    users_id_list = []
    for user in response.json()['users']:
        users_id_list.append(user['id'])

    return response, users_id_list
    
def get_sub_session(sub_session):
    response = requests.get(base_url + '/api/bot/session/' + str(bot_session_id) + '/' + str(sub_session), headers=header)
    return response, SubSessionDataset(response.json())
    
def submit_injection(sub_session, posts_submission, users_submission):
    return requests.post(base_url + '/api/bot/session/' + str(bot_session_id) + '/' + str(sub_session), headers=header, data=json.dumps({"posts": posts_submission, "users": users_submission}))

# DETECTOR SECTION
class SessionDataset:
    def __init__(self, data):
        self.session_id = data["id"]
        self.metadata = data["metadata"]
        self.posts = data["posts"]
        self.users = data["users"]

def get_session_data():
    response = requests.get(base_url + '/api/detector/session/' + str(detector_session_id), headers=header)
    return response, SessionDataset(response.json())
    
def submit_detection(detections_submission):
    return requests.post(base_url + '/api/detector/session/' + str(detector_session_id), headers=header, data=json.dumps({"users": detections_submission}))