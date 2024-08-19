from pydantic import BaseModel, conint, constr
from typing import Optional, Literal

class NewUser(BaseModel): # Should we give this file to the teams or should we only give them a description of the one that they are going to use or should I make two different files? One for the teams and one for us? At this point do I also need to separate it between bot and detector?
    username: str
    name: str
    description: Optional[str] = ""
    location: str

class User(BaseModel):
    user_id: constr(min_length=1)
    username: constr(min_length=1) #Check which one needs to be non empty and which one can be optional. For now other than description all are required and nonempty.
    name: constr(min_length=1)
    description: Optional[str] = ""
    location: str

    def to_dict(self):
        return {
            "id": self.user_id,
            "tweet_count": 1,
            "z_score": 0,
            "username": self.username,
            "name": self.name,
            "description": self.description,
            "location": self.location
        }
        

class NewPost(BaseModel):
    text: str
    author_id: constr(min_length=1) # Maybe make this one optional and just ask them for the user and add ourselves author id later
    created_at: str # Time format like this 2024-03-27T00:06:30.000Z
    lang: Literal['en', 'fr']
    user: User

    def to_dict(self):
        return {
            "id": "123",
            "text": self.text,
            "author_id": self.author_id,
            "created_at": self.created_at,
            "lang": self.lang,
            "user": self.user.to_dict() # Wait right now something weird is that if we give more to the submission, like this line, the part of code of Aviv do not throw an error, it still takes it. Also we really need to talk with Aviv to make everything uniform.
        }

class Post(BaseModel):
    post_id: constr(min_length=1)
    text: str
    author_id: constr(min_length=1)
    created_at: str
    lang: Literal['en', 'fr']
    user: User

class DetectionMark(BaseModel):
    userId: constr(min_length=1) #Change userId to user_id
    confidence: conint(ge=0, le=100)
    bot: bool #Add this one to be able to request from them to tell us if they think an account is actually a bot or not

    def to_dict(self):
        return {
            "userId": self.userId,
            "confidence": self.confidence,
            "bot": self.bot
        }