import json
from abs_classes import ABot
from teams_classes import NewUser, NewPost

class Bot(ABot):
    def create_user(self, session_info):
        # Implement logic here and replace the return value with the number of users you want to create.
        # Example:
        new_users = [
            NewUser(username="Em0", name="Emily", description="I'm a great bot that loves to post about pandas.", location="New Brunswick"),
            NewUser(username="Em2", name="Annabelle", location="The wonderful land of pony")
        ]
        return new_users

    def generate_content(self, datasets_json, users_list):
        # Implement your code to process the datasets here.
        # It needs to return json with the users and their description and the posts to be inserted.
        # Example:
        posts = []
        for j in range(len(users_list)):
            posts.append(NewPost(text="Pandas are amazing!", author_id=users_list[j].user_id, created_at='2024-08-18T00:20:30.000Z', lang='en',user=users_list[j]))
            posts.append(NewPost(text="What's up dude, I'm a bot", author_id=users_list[j].user_id, created_at='2024-08-18T00:22:30.000Z', lang='en',user=users_list[j]))
        return posts
