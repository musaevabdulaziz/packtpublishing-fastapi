from fastapi import APIRouter, status, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from datetime import datetime
from uuid import uuid1

from login.model import SignUp, User, Tourist, approved_users, pending_users
from background import audit_log_transaction


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)


@router.post("/signup")
async def signup(signup: SignUp):
    try:
        userid = uuid1()
        login = User(id=userid, username=signup.username, password=signup.password)
        tourist = Tourist(id=userid, login=login, date_signed=datetime.now(), booked=0, tours=list())
        tourist_json = jsonable_encoder(tourist)
        pending_users[userid] = tourist_json
        return JSONResponse(content=tourist_json, status_code=status.HTTP_201_CREATED)
    except:
        return JSONResponse(content={"message": "invalid operation"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/login")
async def login(login: User, bg_task: BackgroundTasks):
    try:
        signup_json = jsonable_encoder(approved_users[login.id])
        bg_task.add_task(audit_log_transaction, touristId=str(login.id), message="login")
        return JSONResponse(content=signup_json, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={"message": "invalid operation"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/login/{username}/{password}")
async def login_with_credentials(username: str, password: str, bg_task: BackgroundTasks):
    tourist_list = [t for t in approved_users.values() if t["login"]["username"] == username and t["login"]["password"] == password]
    if len(tourist_list) == 0 or tourist_list is None:
        return JSONResponse(content={"message": "invalid operation"}, status_code=status.HTTP_403_FORBIDDEN)
    
    tourist = tourist_list[0]
    tour_json = jsonable_encoder(tourist)
    bg_task.add_task(audit_log_transaction, touristId=str(tourist["login"]["id"]), message="login")
    return JSONResponse(content=tour_json, status_code=status.HTTP_200_OK)
