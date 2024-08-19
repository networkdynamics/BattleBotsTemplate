import requests
from constants import bot_session_id, detector_session_id
import json

# Environment Variables
base_url = 'http://localhost:3000'
# Bot authentication_token
#authentication_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiIzIiwidGVhbU5hbWUiOiJFbWlsaWUgQm90IiwiaWF0IjoxNzI0MDI5NTAyLCJleHAiOjE3MjQxMTU5MDJ9.CU-2YGkkU-i6YVK3zZNfFo4mbtIwSJ6biaGLwuRgMlY'
# Detector authentication_token
authentication_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWFtSWQiOiI0IiwidGVhbU5hbWUiOiJFbWlsaWUgRGV0ZWN0b3IiLCJpYXQiOjE3MjQwMjAzNDMsImV4cCI6MTcyNDEwNjc0M30.kBwhxS5Xr_mjt4fZNIDPUUin-cAWdFVNmOTyYS0L3Jg'
header = {'Authorization': 'bearer ' + authentication_token, 'Content-Type': 'application/json'}

class BotRequests:
    def get_session_info():
        return requests.get(base_url + '/api/bot/session/' + str(bot_session_id) + '/info', headers=header)
    def create_user_id(number_users):
        return requests.post(base_url + '/api/bot/session/' + str(bot_session_id) + '/createuser', headers=header, data=json.dumps({"num_of_users": number_users}))
    def get_sub_session(sub_session):
        return requests.get(base_url + '/api/bot/session/' + str(bot_session_id) + '/' + str(sub_session), headers=header)
    def submit_injection(sub_session, posts_submission, users_submission):
        return requests.post(base_url + '/api/bot/session/' + str(bot_session_id) + '/' + str(sub_session), headers=header, data=json.dumps({"posts": posts_submission, "users": users_submission}))

class DetectorRequests:
    def get_session_data():
        return requests.get(base_url + '/api/detector/session/' + str(detector_session_id), headers=header) 
    def submit_detection(detections_submission):
        return requests.post(base_url + '/api/detector/session/' + str(detector_session_id), headers=header, data=json.dumps({"users": detections_submission}))