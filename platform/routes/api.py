from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
import os, requests, database
from userclass import UserClass
from datetime import datetime
from itsdangerous import Signer, BadSignature
from dotenv import load_dotenv
load_dotenv("../.env")
templates = Jinja2Templates(directory="templates")
signer = Signer(os.getenv("cookie_secret"))

router = APIRouter()

usersdatabase = database.database(os.getenv("databaseurl"))
def get_current_user(request: Request):
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        return None
    try:
        username = signer.unsign(session_cookie.encode()).decode()
        if usersdatabase.checkuser(None,username):
            return username
        return None
    except BadSignature:
        return None
@router.get("/api/currentuserdata")
def currentuserdata(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    user_data = usersdatabase.getuserdetails(email=user)    
    if "_id" in user_data:
        user_data["_id"] = str(user_data["_id"])
    return JSONResponse(content=user_data)