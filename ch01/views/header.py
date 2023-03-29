from fastapi import APIRouter, Header, Response, Cookie
from uuid import UUID
from views.user import request_headers, cookies


router = APIRouter()


@router.get("header/verify")
async def verify_headers(host: str | None = Header(None),
                         accept: str | None = Header(None),
                         accept_language: str | None = Header(None),
                         accept_endoing: str | None = Header(None),
                         user_agent: str | None = Header(None)):
    request_headers["Host"] = host
    request_headers["Accept"] = accept
    request_headers["Accept-Language"] = accept_language
    request_headers["Accept-Encoding"] = accept_endoing
    request_headers["User-Agent"] = user_agent
    return request_headers


@router.get("/cookies")
async def access_cookie(userkey: str | None = Cookie(None), identity: str | None = Cookie(None)):
    cookies["userkey"] = userkey
    cookies["identity"] = identity
    return cookies


@router.post("/rememberme/create")
async def create_cookies(resp: Response, id: UUID, username: str = ""):
    resp.set_cookie(key="userkey", value=username)
    resp.set_cookie(key="identity", value=str(id))
    return {"message": "remember-me tokens created"}