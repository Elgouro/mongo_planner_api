from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from models.event import Event

class User(Document):
    email: EmailStr
    password:str
    events:Optional[List[Link[Event]]]
    class Settings:
        name = "users"
    class Config:
        json_schema_extra= {
            "example":{
                "email": "fastapi@growthentech.com",
                "password":"strong!!!",
                "events" : []
            }
        }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str
    