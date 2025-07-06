from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from userclass import UserClass
from dotenv import load_dotenv
load_dotenv()  
import os,requests,database
from datetime import datetime
from itsdangerous import Signer, BadSignature
signer = Signer(os.getenv("cookie_secret"))
app = FastAPI()
from routes import api
app.include_router(api.router,tags=["api"])
usersdatabase = database.database(os.getenv("databaseurl"))
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/error", response_class=HTMLResponse)
async def error(err:str):
    errors ={
        "userexists": "User already exists",
        "invalidcaptcha": "Invalid Captcha",
        "invalidcredentials": "Invalid username or password",
    }
    if err in errors:
        return JSONResponse({"error": errors[err]})
    else:
        return JSONResponse({"error": "Unknown error occurred"})
    
@app.get("/login", response_class=HTMLResponse)
async def index(request: Request, status: bool = False):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request,"sitekey": os.getenv("sitekey"),"status": status})
@app.post("/login", response_class=HTMLResponse)
async def loginpost(request: Request, email:str=Form(...),password: str = Form(...), recaptcha_response: str = Form(alias="g-recaptcha-response")):
    payload = {
        "secret": os.getenv("secretkey"),
        "response": recaptcha_response
    }
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    result = response.json()
    if not result["success"]:
        return RedirectResponse(url="/error?err=invalidcaptcha",status_code=303)
    if not usersdatabase.validateuser(email, password):
        return RedirectResponse(url="/error?err=invalidcredentials",status_code=303)
    response = RedirectResponse(url="/dashboard", status_code=303)
    signed_username = signer.sign(email.encode()).decode()
    response.set_cookie(
        key="session",
        value=signed_username,
        httponly=True,
        secure=False, 
        samesite="lax",
        max_age=60 * 60 * 24 * 7 
    )
    return response
@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request,status: bool = False):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request,"sitekey": os.getenv("sitekey"),"status": status})
@app.post("/signup")
async def signuppost(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    recaptcha_response: str = Form(alias="g-recaptcha-response") 
):
    payload = {
        "secret": os.getenv("secretkey"),
        "response": recaptcha_response
    }
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    result = response.json()
    if not result["success"]:
        return RedirectResponse(url="/error?err=invalidcaptcha",status_code=303)
    if usersdatabase.checkuser(username, email):
        return RedirectResponse(url="/error?err=userexists",status_code=303)
    user = UserClass(
        username=username,
        email=email,
        password=password,
        created_at=int(datetime.now().timestamp()),
    )
    usersdatabase.adduser(user)
    return RedirectResponse(url="/signup?status=true", status_code=303)
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("session")
    return response




@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    user_data = usersdatabase.getuserdetails(email=user)
    if "_id" in user_data:
        user_data["_id"] = str(user_data["_id"])
    return templates.TemplateResponse("dashboard.html", {"request": request, "userdata": user_data})
@app.get("/trade")
async def trade(request: Request,symbol: str,timeframe: int = 60):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    user_data = usersdatabase.getuserdetails(email=user)
    if "_id" in user_data:
        user_data["_id"] = str(user_data["_id"])
    return templates.TemplateResponse("trade.html", {"request": request, "userdata": user_data,"priceapiurl": os.getenv("priceapiurl"),"symbol": symbol if symbol else "XAUUSD.r","timeframe": timeframe})
@app.get("/tradetest")
async def tradetest(request: Request,symbol: str,timeframe: int = 60):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    user_data = usersdatabase.getuserdetails(email=user)
    if "_id" in user_data:
        user_data["_id"] = str(user_data["_id"])
    return templates.TemplateResponse("tradetest.html", {"request": request, "userdata": user_data,"priceapiurl": os.getenv("priceapiurl"),"symbol": symbol if symbol else "XAUUSD.r","timeframe": timeframe})