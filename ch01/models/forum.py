from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from models.post import PostType
from models.user import UserProfile


class ForumPost(BaseModel):
    id: UUID
    topic: str | None = None
    message: str
    post_type: PostType
    date_posted: datetime
    username: str


class ForumDiscussion(BaseModel):
    id: UUID
    main_post: ForumPost
    replies: list[ForumPost] | None = None
    author: UserProfile