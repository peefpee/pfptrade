from pydantic import BaseModel
class position(BaseModel):
    id: int 
    userid: int
    symbol: str
    size: float
    openprice: float
    closeprice: float
    opentime: int
    closetime: int
    trade_type: int # 0 for buy, 1 for sell
    takeprofit: float = None
    stoploss: float = None
    comment: str = ""
class historytrade(BaseModel):
    id: int 
    userid: int
    symbol: str
    size: float
    openprice: float
    closeprice: float
    opentime: int
    closetime: int
    trade_type: int # 0 for buy, 1 for sell
    takeprofit: float = None
    stoploss: float = None
    hittpsl : int = 0 # 0 for not hit, 1 for hit take profit, 2 for hit stop loss
    grossprofit: float
    netprofit: float
    commission: float = 0.0
    comment: str = ""
class order(BaseModel):
    type: int # 0 for market, 1 for limit, 2 for stop
    id: int
    userid: int
    symbol: str
    size: float
    price : float = None
    status: int # 0 for filled,1 for pending 2 for cancelled
    created_at: int
    filled_at: int = None
    cancelled_at: int = None
    takeprrofit: float = None
    stoploss: float = None
    comment: str = ""
    trade_type: int # 0 for buy, 1 for sell

    
