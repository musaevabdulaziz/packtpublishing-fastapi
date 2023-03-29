from fastapi import FastAPI

from views.account import router as account
from views.header import router as header
from views.login import router as login
from views.post import router as post
from views.unlock import router as unlock
from views.user import router as user


app = FastAPI()
app.include_router(user)
app.include_router(account)
app.include_router(post)
app.include_router(login)
# app.include_router(unlock)
app.include_router(header)


# valid_users = dict()
# pending_users = dict()
# valid_profiles = dict()
# discussion_posts = dict()




# @app.get("/ch01/index")
# async def index():
#     return {"message": "Welcome FastAPI nerds"}


# @app.get("/ch01/login/details/info")
# async def login_info():
#     return {"message": "username and password are needed"}


# @app.get("/ch01/login")
# async def login(username: str, password: str):
#     if valid_users.get(username) == None:
#         return {"message": "user does not exist"}

#     user = valid_users.get(username)

#     if checkpw(password.encode(), user.passphrase.encode()):
#         return user

#     return {"message": "invalid user"}


# @app.post("/ch01/login/signup")
# async def signup(uname: str, passwd: str):
#     if (uname is None) and (passwd is None):
#         return {"message": "invalid user"}

#     if valid_users.get(uname) is not None:
#         return {"message": "user exists"}
    
#     user = User(username=uname, password=passwd)
#     pending_users[uname] = user
#     return user


# @app.put("ch01/account/profile/update/{username}")
# async def update_profile(username: str, id: UUID, new_profile: UserProfile):
#     if valid_users.get(username) is None:
#         return {"message": "user does not exist"}

#     user = valid_users.get(username)

#     if user.id == id:
#         valid_profiles[username] == new_profile
#         return {"message": "successfully updated"}

#     return {"message": "user does not exist"}


# @app.patch("ch01/account/profile/update/names/{username}")
# async def update_profile_names(username: str, id: UUID, new_names: dict[str, str]):
#     if valid_users.get(username) is None:
#         return {"message": "user does not exist"}
#     elif new_names is None:
#         return {"message": "new names are required"}
#     else:
#         user = valid_users.get(username)

#         if user.id == id:
#             profile = valid_profiles[username]
#             profile.firstname = new_names["fname"]
#             profile.lastname = new_names["lname"]
#             profile.middle_initial = new_names["mi"]
#             valid_profiles[username] = profile
#             return {"message": "successfully updated"}

#         return {"message": "user does not exist"}
        

# @app.delete("/ch01/discussion/posts/remove/{username}")
# async def delete_discussion(username: str, id: UUID):
#     if valid_users.get(username) is None:
#         return {"message": "user does not exist"}
    
#     if discussion_posts.get(id) is None:
#         return {"message": "post does not exist"}

#     del discussion_posts[id]
#     return {"message": "main post deleted"}

# """
# additional apis
# """
# @app.delete("/ch01/login/remove/{username}")
# async def delete_user(username: str):
#     if username is None:
#         return {"message" "invalid user"}

#     del valid_users[username]
#     return {"message": "user deleted"}


# @app.delete("/ch01/login/remove/all")
# async def delete_users(usernames: list[str]):
#     for user in usernames:
#         del valid_users[user]
#     return {"message": "users deleted"}


# @app.get("/ch01/login/{username}/{password}")
# async def login_with_token(username: str, password: str, id: UUID):
#     if valid_users.get(username) is None:
#         return {"message": "user does not exist"}

#     user = valid_users[username]
#     if user.id == id and checkpw(password.encode(), user.passphrase()):
#         return user
#     return {"message": "invalid user"}