from pydantic import BaseModel

from uuid import UUID

from places.model import Post


class Assessment(BaseModel):
    id: UUID
    post: Post
    tour_id: UUID
    tourist_id: UUID


feedback_tour = dict()