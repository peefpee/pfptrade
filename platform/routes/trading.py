from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os, requests, database
from userclass import UserClass
import usertrading
from datetime import datetime
from itsdangerous import Signer, BadSignature
import symbols
from dotenv import load_dotenv
load_dotenv("../.env")
templates = Jinja2Templates(directory="templates")
signer = Signer(os.getenv("cookie_secret"))
router = APIRouter()
usersdatabase = database.database(os.getenv("databaseurl"))
import tradeclass
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
@router.post("/trade/new/market")
async def new_trade(request: Request, symbol: str = Form(...), size: float = Form(...),trade_type: int = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    user_data = usersdatabase.getuserdetails(email=user)
    if not user_data:
        return JSONResponse(content={"error": "User not found","Success":False}, status_code=404)
    leverage = user_data.leverage if hasattr(user_data, 'leverage') else 1
    if size <= 0:
        return JSONResponse(content={"error": "Size must be greater than 0","Success":False}, status_code=400)
    if symbol not in symbols.symbolinfo:
        return JSONResponse(content={"error": "Invalid symbol","Success":False}, status_code=400)
    symbol_data = symbols.symbolinfo[symbol]
    price = requests.get(f"{os.getenv('priceapiurl')}/api/price/{symbol}").json()
    if trade_type == 0:
        price = price["ask"]
    elif trade_type == 1:
        price = price["bid"]
    if size > user_data.balance * leverage / price:
        return JSONResponse(content={"error": "Insufficient balance"}, status_code=400)
    order = tradeclass.order(
        id=usertrading.usertrading(user_data).nexttradeid(),
        userid=user_data.id,
        symbol=symbol,
        size=size,
        status=1,
        created_at=int(datetime.now().timestamp()),
        type=0,
        trade_type=trade_type)
    usersdatabase.addorder(user_data.id,order)  
    return JSONResponse(content={"message": "Order created successfully", "order_id": order.id,"Success":True}, status_code=201)
        
    