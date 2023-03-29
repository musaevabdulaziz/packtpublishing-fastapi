from pydantic import BaseModel

from datetime import datetime
from uuid import UUID


approved_users = dict()
pending_users = dict()


class SignUp(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    birthday: datetime


class User(BaseModel):
    id: UUID
    username: str
    password: str


class Tourist(BaseModel):
    id: UUID
    username: str
    password: str