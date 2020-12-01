import os
import json
import asyncio
import websockets
import time
from .config import schema


async def ping():
    uri = f"{schema}://{os.environ['SERVER_HOST']}/ws/{os.environ['CLIENT_ID']}"
    async with websockets.connect(
        uri,
    ) as websocket:
        while True:
            param = {"type": "pong"}
            await websocket.send(json.dumps(param))
            print(f"> {param}")

            greeting = await websocket.recv()
            print(f"< {greeting}")
            time.sleep(1)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(ping())
