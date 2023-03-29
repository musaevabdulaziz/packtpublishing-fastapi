from fastapi import APIRouter
from uuid import UUID

from views.user import valid_users


router = APIRouter(
    prefix="/unlock"
)


@router.post("/username")
async def unlock_username(id: UUID | None = None):
    if id is None:
        return {"message": "token needed"}

    for key, val in valid_users.items():
        if val.id == id:
            return {"username": val.username}
    return {"message": "user name does not exist"}


@router.post("/password")
async def unlock_password(username: str | None = None, id: UUID | None = None):
    if username is None:
        return {"message": "username is required"}
    
    elif valid_users.get(username) == None:
        return {"message": "user does not exist"}
    
    else:
        if id is None:
            return {"message": "token needed"}
        
        user = valid_users.get(username)
        if user.id == id:
            return {"password": user.password}
        
        return {"message": "invalid token"}