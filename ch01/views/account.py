from fastapi import APIRouter, Form
from datetime import datetime
from uuid import UUID

from models.user import UserProfile, UserType
from views.user import valid_users, valid_profiles


router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}}
)


@router.post("/profile/add", response_model=UserProfile)
async def add_profile(uname: str,
                      fname: str = Form(),
                      lname: str = Form(),
                      mid_init: str = Form(),
                      user_age: int = Form(),
                      sal: float = Form(),
                      bday: str = Form(),
                      utype: UserType = Form()):
    
    if valid_users.get(uname) is None:
        return UserProfile(firstname=None, 
                           lastname=None, 
                           middle_initial=None, 
                           age=None, 
                           birthday=None, 
                           salary=None, 
                           user_type=None)
    
    profile = UserProfile(firstname=fname, 
                          lastname=lname, 
                          middle_initial=mid_init, 
                          age=user_age, 
                          birthday=datetime.strptime(bday, '%m/%d/%Y'), 
                          salary=sal, 
                          user_type=utype)
    valid_profiles[uname] = profile
    return profile


@router.get("/profile/view/{username}")
async def access_profile(username: str, id: UUID):
    if valid_users.get(username) is None:
        return user_does_not_exist()

    user = valid_users.get(username)
    if user.id == id:
        return valid_profiles[username]
    return user_does_not_exist()

    
@router.put("/profile/update/{username}")
async def update_profile(username: str, id: UUID, new_profile: UserProfile):
    if valid_users.get(username) == None:
        return user_does_not_exist()

    user = valid_users.get(username)
    if user.id == id:
        valid_profiles[username] = new_profile
        return {"message": "successfully updated"}
    
    return user_does_not_exist()
    

@router.patch("/update/names/{username}")
async def update_profile_names(id: UUID, username: str = "", new_names: dict[str, str] | None = None):
    if valid_users.get(username) == None:
        return user_does_not_exist()
    
    if new_names == None:
        return {"message": "new names are required"}
    
    user = valid_users.get(username)

    if user.id == id:
        profile = valid_profiles[username]
        profile.firstname = new_names["fname"]
        profile.lastname = new_names["lname"]
        profile.middle_initial = new_names["mi"]
        valid_profiles[username] = profile
        return {"message": "successfully updated"}
        
    return user_does_not_exist()


# helper methods
def user_does_not_exist():
    return {"message": "user does not exist"}