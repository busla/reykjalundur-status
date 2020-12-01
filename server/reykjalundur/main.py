import os
import json
import logging
from typing import List
from datetime import datetime
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    Request,
)
from fastapi.logger import logger
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocket

from reykjalundur.common.models import (
    EmailMessage,
    SocketResponse,
)
from reykjalundur.settings import settings
from reykjalundur.common.email import send_mail

app = FastAPI()
app.mount("/static", StaticFiles(directory="server/reykjalundur/static"), name="static")
templates = Jinja2Templates(directory="server/reykjalundur/templates")
logging.basicConfig(level=logging.DEBUG)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "host": os.environ["SERVER_HOST"]}
    )


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    if client_id == os.environ["CLIENT_ID"]:
        await send_mail(EmailMessage(**settings.message_reconnect))
    try:
        while True:
            await websocket.receive_text()

            payload = SocketResponse(
                **{
                    "message": f"{client_id} reporting",
                    "current_time": datetime.now(),
                    "status": 1,
                }
            )
            await manager.broadcast(payload.json())
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        payload = SocketResponse(
            **{
                "message": f"{client_id} left",
                "current_time": datetime.now(),
                "status": 0,
            }
        )
        await manager.broadcast(payload.json())
        await send_mail(EmailMessage(**settings.message_disconnect))
