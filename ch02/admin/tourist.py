from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from login.model import approved_users, pending_users


router = APIRouter(
    prefix="/tourist"
)


@router.get("/list")
async def list_all_tourists():
    return approved_users


@router.get("/list/pending")
async def list_all_pending_tourists():
    return pending_users


@router.get("/vip")
async def list_valuable_visitors():
    try:
        sort_orders = sorted(approved_users.items(), key=lambda x: x[1].booked, reverse=True)
        sorted_orders_json = jsonable_encoder(sort_orders)
        return JSONResponse(content=sorted_orders_json, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={"message": "invalid operation"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)