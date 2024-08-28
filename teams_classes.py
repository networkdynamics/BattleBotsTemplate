from pydantic import BaseModel, conint, constr, Field
from typing import Optional

class NewUser(BaseModel): # Should we give this file to the teams or should we only give them a description of the one that they are going to use or should I make two different files? One for the teams and one for us? At this point do I also need to separate it between bot and detector?
    username: constr(min_length=1)
    name: constr(min_length=1)
    description: Optional[str] = ""
    location: Optional[str] = None

class User(BaseModel):
    user_id: constr(min_length=1)
    username: constr(min_length=1) #This one unique
    name: constr(min_length=1)
    description: Optional[str] = ""
    location: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.user_id,
            "tweet_count": 0,
            "z_score": 0,
            "username": self.username,
            "name": self.name,
            "description": self.description,
            "location": self.location
        }
        

class NewPost(BaseModel):
    text: constr(min_length=1)
    author_id: constr(min_length=1)
    created_at: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000Z$') # Time format like this 2024-03-27T00:06:30.000Z

    def to_dict(self, dataset_lang):
        return {
            "id": "",
            "text": self.text,
            "author_id": self.author_id,
            "created_at": self.created_at,
            "lang": dataset_lang,
        }

class DetectionMark(BaseModel):
    user_id: constr(min_length=1)
    confidence: conint(ge=0, le=100)
    bot: bool

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "confidence": self.confidence,
            "bot": self.bot
        }