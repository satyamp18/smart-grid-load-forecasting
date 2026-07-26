from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from smartgrid.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws/alerts")
async def websocket_endpoint(
    websocket: WebSocket,
):

    await manager.connect(websocket)

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(websocket)

    except Exception:

        manager.disconnect(websocket)