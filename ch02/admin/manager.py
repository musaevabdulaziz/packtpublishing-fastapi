from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from uuid import UUID

from admin.destination import router as destination
from admin.tourist import router as tourist
from login.model import approved_users, pending_users


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}}
)
router.include_router(destination)
router.include_router(tourist)


@router.post("/user/login/approve")
async def approve_login(userid: UUID):
    try:
        approved_users[userid] = pending_users[userid]
        del pending_users[userid]
        return JSONResponse(content={"message": "user approved"}, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={"message": "invalid operatin"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)