from pydantic import BaseModel
from uuid import UUID
from enum import Enum
from datetime import date


class User(BaseModel):
    username: str
    password: str


class ValidUser(BaseModel):
    id: UUID
    username: str
    password: str
    passphrase: str


class UserType(str, Enum):
    admin = "admin"
    teacher = "teacher"
    alumni = "alumni"
    student = "student"


class UserProfile(BaseModel):
    firstname: str
    lastname: str
    middle_initial: str
    age: int | None = 0
    salary: int | None = 0
    birthday: date
    user_type: UserType