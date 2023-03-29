from pydantic import BaseModel
from typing import NamedTuple

from datetime import datetime
from uuid import UUID
from enum import Enum, IntEnum


tours = dict()
tours_basic_info = dict()
tours_location = dict()


class StarRating(IntEnum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5


class Post(BaseModel):
    feedback: str
    rating: StarRating
    date_posted: datetime


class Location(NamedTuple):
    latitude: float
    longitude: float = 0.0


class TourType(str, Enum):
    resort = "resort"
    hotel = "hotel"
    bungalow = "bungalow"
    tent = "tent"
    exclusive = "exclusive"


class AmenitiesTypes(str, Enum):
    restaurant = "restaurant"
    pool = "pool"
    beach = "beach"
    shops = "shops"
    bars = "bars"
    activities = "activities"


class TourInput(BaseModel):
    name: str
    city: str
    country: str
    type: TourType
    location: Location
    amenities: list[AmenitiesTypes]


class Tour(BaseModel):
    id: UUID
    name: str
    city: str
    country: str
    type: TourType
    location: Location
    amenities: list[AmenitiesTypes]
    feedbacks: list[Post]
    ratings: float
    visits: int
    isBooked: bool


class TourBasicInfo(BaseModel):
    id: UUID
    name: str
    type: TourType
    amenities: list[AmenitiesTypes]
    ratings: float


class TourLocation(BaseModel):
    id: UUID
    name: str
    city: str
    country: str
    location: Location


class TourPreference(str, Enum):
    party = "party"
    extreme = "extreme"
    staycation = "staycation"
    groups = "groups"
    solo = "solo"