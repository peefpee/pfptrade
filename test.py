import asyncio
import websockets
import json

async def listen_ticks(symbol="XAUUSD.r"):
    url = f"ws://localhost:8001/api/ws/ticks/{symbol}"

    async with websockets.connect(url) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received tick: {data['symbol']} Bid: {data['bid']} Ask: {data['ask']}")

asyncio.run(listen_ticks())
