from fastapi import APIRouter, HTTPException, status

from datetime import datetime
from uuid import UUID, uuid1

from places.model import TourBasicInfo, TourPreference, tours, tours_location
from tourist.model import Visit, Booking, tour_preferences
from login.model import approved_users


router = APIRouter(
    prefix="/tourist/tour",
    tags=["tour"],
    responses={404: {"description": "Not found"}}
)


@router.get("/preference")
async def make_tour_preferences(preference: TourPreference):
    tour_preferences.add(preference)
    return tour_preferences


@router.post("/booking/add")
async def create_booking(tour: TourBasicInfo, touristId: UUID):
    if approved_users.get(touristId) is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="details are missing")

    booking = Booking(id=uuid1(), destination=tour, booking_date=datetime.now(), tourist_id=touristId) 
    print(approved_users[touristId])
    approved_users[touristId]["tours"].append(tour)
    approved_users[touristId]["booked"] += 1
    tours[tour.id].isBooked = True
    tours[tour.id].visits += 1
    return booking


@router.delete("/booking/delete")
async def remove_booking(bid: UUID, touristId: UUID):
    if approved_users.get(touristId) is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="details are missing")
    new_booking_list = [booked for booked in approved_users[touristId]["tours"] if booked.id == bid]
    approved_users[touristId]["tours"] = new_booking_list
    return approved_users[touristId]


@router.get("/booked")
async def show_booked_users(touristId: UUID):
    if approved_users.get(touristId) is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="details are missing", headers={"X-InputError": "missing tourist ID"})
    return approved_users[touristId]["tours"]


@router.get("/location")
async def show_location(tid: UUID):
    return tours_location[tid]


@router.get("/available")
async def show_available_tours():
    available_tours =[t for t in tours.values() if not t.isBooked]
    return available_tours