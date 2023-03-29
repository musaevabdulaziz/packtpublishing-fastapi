from pydantic import BaseModel

from datetime import datetime
from uuid import UUID

from places.model import TourBasicInfo


class Visit(BaseModel):
    id: UUID
    destination: list[TourBasicInfo]
    last_tour: datetime


class Booking(BaseModel):
    id: UUID
    destination: TourBasicInfo
    booking_date: datetime
    tourist_id: UUID


tour_preferences = set()