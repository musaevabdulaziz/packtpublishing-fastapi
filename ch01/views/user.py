from fastapi import APIRouter
from uuid import uuid1 
from bcrypt import hashpw, gensalt

from models.user import User, ValidUser


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


valid_users = dict()
valid_profiles = dict()
pending_users = dict()
discussion_posts = dict()
request_headers = dict()
cookies = dict()


@router.get("/index")
async def index():
    return {"message": "Welcome FastAPI nerds"}


@router.post("/login/signup")
async def signup(uname: str, passwd: str):
    if (uname is None) and (passwd is None):
        return {"message": "invalid user"}

    if valid_users.get(uname) is not None:
        return {"message": "user exists"}

    user = User(username=uname, password=passwd)
    pending_users[uname] = user
    return user


@router.get("/list/users/pending")
async def list_pending_users():
    return pending_users


@router.delete("/delete/users/pending")
async def delete_pending_users(accounts: list[str] = []):
    for user in accounts:
        del pending_users[user]

    return {"message": "pending users deleted"}


@router.post('/login/validate', response_model=ValidUser)
async def approve_user(user: User):
    if valid_users.get(user.username) is not None:
        return ValidUser(id=None, username=None, password=None, passphrase=None)

    valid_user = ValidUser(id=uuid1(), username=user.username, password=user.password, passphrase=hashpw(user.password.encode(), gensalt()))
    valid_users[user.username] = valid_user
    del pending_users[user.username]
    return valid_user


@router.delete("/login/remove/all")
async def delete_users(usernames: list[str]):
    for user in usernames:
        del valid_users[user]
    return {"message": "users deleted"}


@router.delete("/login/remove/{username}")
async def delete_user(username: str):
    if username == None:
        return {"message": "user invalid"}

    del valid_users[username]
    return {"message": "user deleted"}


@router.get("/list/users/valid")
async def list_valid_users():
    return valid_users