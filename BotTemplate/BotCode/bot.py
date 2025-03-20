from abc_classes import ABot
from teams_classes import NewUser, NewPost

class Bot(ABot):
    # This global_session_info is just used for the example code, feel free to remove it
    global_session_info = None
    def create_user(self, session_info):
        # todo logic
        # Example:
        global global_session_info
        global_session_info = session_info

        new_users = [
            NewUser(username="TestBot", name="Bot2.0", description="Hello I'm a bot")
        ]
        return new_users

    def generate_content(self, datasets_json, users_list):
        # todo logic
        # It needs to return json with the users and their description and the posts to be inserted.
        # Example:
        global global_session_info

        posts = []
        for j in range(len(users_list)):
            posts.append(NewPost(text="Pandas are amazing!", author_id=users_list[j].user_id, created_at=global_session_info.sub_sessions_info[datasets_json.sub_session_id-1]["start_time"],user=users_list[j]))
            posts.append(NewPost(text="Hello World 2025!", author_id=users_list[j].user_id, created_at=global_session_info.sub_sessions_info[datasets_json.sub_session_id-1]["start_time"],user=users_list[j]))
            posts.append(NewPost(text="I'm a bot. Hello.", author_id=users_list[j].user_id, created_at=global_session_info.sub_sessions_info[datasets_json.sub_session_id-1]["end_time"],user=users_list[j]))
        return posts
