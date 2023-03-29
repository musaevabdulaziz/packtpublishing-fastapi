from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as GlobalStarletteHTTPException

from datetime import datetime

from admin.manager import router as admin
from feedback.router import router as feedback
from login.router import router as login
from places.router import router as places
from tourist.router import router as tourist
from handler_exceptions import PostFeedbackException, PostRatingException


app = FastAPI()
app.include_router(admin)
app.include_router(feedback)
app.include_router(login)
app.include_router(places)
app.include_router(tourist)


@app.middleware("http")
async def log_transaction_filter(request: Request, call_next):
    start_time = datetime.now()
    method_name = request.method
    qp_map = request.query_params
    pp_map = request.path_params
    with open("request_log.txt", mode="a") as reqfile:
        content = f"method: {method_name}, query param: {qp_map}, path param: {pp_map} received at {datetime.now()}"
        reqfile.write(content)

    response = await call_next(request)
    process_time = datetime.now() - start_time
    response.headers["X-Time-Elapsed"] = str(process_time)
    return response


@app.get("/ch02")
async def index():
    return {"message": "Intelligent Tourist System Prototype!"}


@app.exception_handler(PostFeedbackException)
async def feedback_exception_handler(req: Request, ex: PostFeedbackException):
    return JSONResponse(status_code=ex.status_code, content={"message": f"error: {ex.detail}"})


@app.exception_handler(PostRatingException)
async def rating_exception_handler(req: Request, ex: PostRatingException):
    return JSONResponse(status_code=ex.status_code, content={"message": f"error: {ex.detail}"})


@app.exception_handler(GlobalStarletteHTTPException)
async def global_exception_handler(req: Request, ex: str):
    return PlainTextResponse(f"Error message: {ex}", status_code=400)


@app.exception_handler(RequestValidationError)
async def validation_error_exception_handler(req: Request, ex: str):
    return PlainTextResponse(f"Error message: {ex}", status_code=400)