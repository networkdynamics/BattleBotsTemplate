import json

def createUser(session_info):
    # Implement logic here
    print(session_info)
    number_user = 2
    return number_user

def subSessionInjection(sub_session_id, datasets_json, users_id):
    print(sub_session_id)
    # Implement your code to process the datasets here.
    # It needs to return json with the users and their description and the posts to be inserted.
    users = []
    posts = []
    for user_id in users_id:
        posts.append({"id": "123", "text": "Hello I'm a bot", "author_id": user_id, "created_at": "8 am", "lang": "en"})
        users.append({"id": user_id, "tweet_count": 1, "z_score": 0, "username": "Em88", "name": "Emilie", "description": "test", "location": "SF"})
    submission_file = {"posts": posts, "users": users}
    return submission_file
