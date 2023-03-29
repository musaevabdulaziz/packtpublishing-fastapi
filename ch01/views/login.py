from fastapi import APIRouter
from bcrypt import checkpw, hashpw, gensalt
from uuid import UUID
from random import choice
from string import ascii_lowercase

from views.user import valid_users
from views.account import user_does_not_exist
from views.unlock import router as unlock


router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}}
)
router.include_router(unlock)


@router.get("/")
async def login(username: str, password: str):
    if valid_users.get(username) == None:
        return user_does_not_exist()

    user = valid_users.get(username)
    if checkpw(password.encode(), user.passphrase.encode()):
        return user
    
    return {"message": "invalid user"}


@router.get("/details/info")
async def login_info():
    return {"message": "username and password are needed"}


@router.get("/password/change")
async def change_password(username: str, old_passw: str = "", new_passw: str = ""):
    passwd_len = 8

    if valid_users.get(username) == None:
        return user_does_not_exist()
    
    if old_passw == "" or new_passw == "":
        characters = ascii_lowercase
        temporary_passwd = "".join(choice(characters) for _ in range(passwd_len))
        user = valid_users.get(username)
        user.password = temporary_passwd
        user.passphrase = hashpw(temporary_passwd.encode(), gensalt())
        return user
    else:
        user = valid_users.get(username)
        if user.password == old_passw:
            user.password = new_passw
            user.passphrase = hashpw(new_passw.encode(),gensalt())
            return user
        return {"message": "invalid user"}



@router.get("/{username}/{password}")
async def login_with_token(username: str, password: str, id: UUID):
    if valid_users.get(username) is None:
        return user_does_not_exist()
    
    user = valid_users.get(username)
    if user.id == id and checkpw(password.encode(), user.passphrase):
        return user
    return {"message": "invalid user"}