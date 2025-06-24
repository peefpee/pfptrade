from fastapi import FastAPI,WebSocket, WebSocketDisconnect
import metatraderconnection
import os,asyncio,json
app = FastAPI()
print(os.getenv("MT5LOGIN"))
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
        symbols = mt5.getallsymbols()
        return {"symbols": symbols}
    except Exception as e:
        return {"error": str(e)}
