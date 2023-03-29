from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class PostType(str, Enum):
    information = "information"
    inquiry = "inquiry"
    quote = "quote"
    twit = "twit"


class Post(BaseModel):
    topic: str | None = None
    message: str
    date_posted: datetime