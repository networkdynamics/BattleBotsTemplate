from abc_classes import ABot
from teams_classes import NewUser, NewPost

class Bot(ABot):
    def create_user(self, session_info):
        # todo logic
        # Example:
        new_users = [
            NewUser(username="TestBot", name="Emilie", description="I'm a test bot."),
        ]
        return new_users

    def generate_content(self, datasets_json, users_list):
        # todo logic
        # It needs to return json with the users and their description and the posts to be inserted.
        # Example:

        posts = []
        for j in range(len(users_list)):
            posts.append(NewPost(text="Pandas are amazing!", author_id=users_list[j].user_id, created_at='2024-08-18T00:20:30.000Z',user=users_list[j]))
        return posts
