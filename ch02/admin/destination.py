from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID, uuid1

from places.model import Tour, TourBasicInfo, TourInput, TourLocation, tours, tours_basic_info, tours_location


router = APIRouter(
    prefix="/destination"
)


@router.get("/list", status_code=status.HTTP_200_OK)
async def list_all_tour_destinations():
    return tours


@router.post("/add")
async def add_tour_destination(input: TourInput):
    try:
        tid = uuid1()
        tour = Tour(id=tid, 
                    name=input.name,
                    city=input.city,
                    country=input.country,
                    type=input.type,
                    location=input.location,
                    amenities=input.amenities,
                    feedbacks=list(),
                    ratings=0.0,
                    visits=0,
                    isBooked=False)
        tour_basic_info = TourBasicInfo(id=tid, name=input.name, type=input.type, amenities=input.amenities, ratings=0.0)
        tour_location = TourLocation(id=tid, name=input.name, city=input.city, country=input.country, location=input.location)
        tours[tid] = tour
        tours_basic_info[tid] = tour_basic_info
        tours_location[tid] = tour_location
        tour_json = jsonable_encoder(tour)
        return JSONResponse(content=tour_json, status_code=status.HTTP_201_CREATED)
    except:
        return JSONResponse(content={"message": "invalid tour"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/update")
async def update_tour_destination(tour: Tour):
    try:
        tid = tour.id
        tours[tid] = tour
        tour_basic_info = TourBasicInfo(id=tid, name=tour.name, type=tour.type, amenities=tour.amenities, ratings=tour.ratings)
        tour_location = TourLocation(id=tid, name=tour.name, city=tour.city, country=tour.country, location=tour.location)
        tours_basic_info[tid] = tour_basic_info
        tours_location[tid] = tour_location
        return {"message": "tour updated"}
    except:
        return {"message": "tour does not exist"}


@router.delete("remove/{id}")
async def remove_tour_destination(id: UUID):
    try:
        del tours[id]
        del tours_basic_info[id]
        del tours_location[id]
        return JSONResponse(content={"message": "tour deleted"}, status_code=status.HTTP_202_ACCEPTED)
    except:
        return JSONResponse(content={"message": "tour does not exist"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
