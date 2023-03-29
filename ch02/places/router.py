from fastapi import APIRouter, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import UUID

from places.model import tours


router = APIRouter(
    prefix="/destination",
    tags=["destination"],
    responses={404: {"description": "Not found"}}
)


@router.get("/list/all")
async def list_tour_destinations():
    tours_json = jsonable_encoder(tours)
    resp_headers = {'X-Access-Tours': 'Try Us', 'X-Contact-Details':'1-900-888-TOLL', 'Set-Cookie':'AppName=ITS; Max-Age=3600; Version=1'}
    return JSONResponse(content=tours_json, headers=resp_headers)


@router.get("/details/{id}")
async def check_tour_profile(id: UUID):
    tour_info_json = jsonable_encoder(tours[id])
    return JSONResponse(content=tour_info_json)


@router.get("/amenities/tour/{id}")
async def show_amenities(id: UUID):
    if tours[id].amenities is not None:
        amenities = tours[id].amenities
        amenities_json = jsonable_encoder(amenities)
        return JSONResponse(content=amenities_json)
    return {"message": "no amenities"}


@router.get("/mostbooked")
async def check_recommended_tour(resp: Response):
    resp.headers['X-Access-Tours'] = 'TryUs'
    resp.headers['X-Contact-Details'] = '1900888TOLL'
    resp.headers['Content-Language'] = 'en-US'
    ranked_desc_rates = sorted(tours.items(), key=lambda x: x[1].ratings, reverse=True)
    return ranked_desc_rates