from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Body
from modules.api.models import *
from modules.api import api
import gradio as gr
from modules.shared import opts,OptionInfo

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.master_websocket = None

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
    
    def setMaster(self, websocket: WebSocket):
        self.master_websocket = websocket
    
    def getMaster(self):
        return self.master_websocket


manager = ConnectionManager()

def ws_api(_: gr.Blocks, app: FastAPI):

    @app.websocket("/ws/master/{master_id}")
    async def websocket_master_endpoint(websocket: WebSocket, master_id: str):
        await websocket.accept()
        manager.setMaster(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(data)
        except WebSocketDisconnect:
            await manager.broadcast(f"{{ type: \"log\", value: \"Master #{master_id} closed\" }}")

    @app.websocket("/ws/client/{client_id}")
    async def websocket_client_endpoint(websocket: WebSocket, client_id: str):
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                master_websocket = manager.getMaster()
                if master_websocket:
                    await master_websocket.send_text(data)
                # print(f"Client #{client_id} received message: {data}")
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            await manager.broadcast(f"{{ type: \"log\", value: \"Client #{client_id} closed\" }}")

try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(ws_api)
except:
    pass
