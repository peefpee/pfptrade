from fastapi import FastAPI,WebSocket, WebSocketDisconnect
import metatraderconnection
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os,asyncio,json
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],  # frontend site origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
mt5 = metatraderconnection.metatrader()
mt5.initialize()

@app.get("/")
def root():
    return {"message": "hello"}




@app.websocket("/api/ws/ticks/{symbol}")
async def websocket_ticks(websocket:WebSocket, symbol: str):
    await websocket.accept()
    try:
        while True:
            tick = mt5.symbol_info_tick(symbol)
            if tick:
                data = {
                    "symbol": symbol,
                    "bid": tick.bid,
                    "ask": tick.ask,
                    "time": tick.time
                }
                await websocket.send_text(json.dumps(data))
            await asyncio.sleep(1) 
    except WebSocketDisconnect:
        print(f"WebSocket disconnected: {symbol}")
@app.get('/api/symbols')
def get_symbols():
    try:
        symbols = mt5.get_all_symbols()
        return {"symbols": symbols}
    except Exception as e:
        return {"error": str(e)}
@app.get("/api/history/{symbol}/{timeframe}")
def get_history(symbol: str, timeframe: int):
    """
    Get historical candles for a symbol and timeframe.
    """
    try:
        mt_timeframe = mt5.timeframe(timeframe)
        candles = mt5.symbol_info_history(symbol, mt_timeframe, count=500)
        return JSONResponse(content=candles)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))