import json
from fastapi import APIRouter, Depends, WebSocket

from app.dto.chat_dto import ChatResponseData, MessageType
from app.helpers.auth_helpers import get_current_user
from app.helpers.exceptions import BadRequestException
from app.services.chat_services import ChatService

router = APIRouter(tags=["Chat meal suggestion"], prefix="/chat")

@router.websocket("/full_response")
async def connect_chat(websocket: WebSocket, user_id: str = Depends(get_current_user)):
    await websocket.accept()

    # Get history and send to client
    history = await ChatService.get_history(user_id)
    history_dict = []
    for msg in history:
        history_dict.append(msg.dict())

    await websocket.send_json(
        {
            "messageType": "HISTORY",
            "message": history_dict,
        }
    )
    await websocket.send_json(
        ChatResponseData(
            message="Hi, how can I help you today?",
            messageType=MessageType.BOT_TEXT,
        ).dict()
    )

    # Wait for message from client
    while True:
        data = await websocket.receive_text()
        messages = await ChatService.chat_suggestion(user_id, data)
        # Response to client
        for msg in messages:
            await websocket.send_json(msg)
        
        # Save history
        await ChatService.save_history(user_id, [ChatResponseData(message=data, messageType=MessageType.USER).dict()])
        await ChatService.save_history(user_id, messages)


@router.websocket("/stream_response")
async def connect_chat_stream(websocket: WebSocket, user_id: str = Depends(get_current_user)):
    await websocket.accept()

    # Get history and send to client
    history = await ChatService.get_history(user_id)
    history_dict = []
    for msg in history:
        history_dict.append(msg.dict())
        
    await websocket.send_json(
        {
            "messageType": "HISTORY",
            "message": history_dict,
        }
    )
    await websocket.send_json(
        ChatResponseData(
            message="Hi, how can I help you today?",
            messageType=MessageType.BOT_TEXT,
        ).dict()
    )

    # Wait for message from client
    while True:
        data = await websocket.receive_text()

        # Response to client
        stream_response = ""
        normal_ressponse = []
        async for chunk in ChatService.chat_stream_response(user_id, data):
            await websocket.send_json(chunk)
            if chunk["messageType"] == MessageType.STREAM:
                stream_response += chunk["message"]
            else:
                normal_ressponse.append(chunk)

        # Save history
        save_history = [
            ChatResponseData(message=data, messageType=MessageType.USER).dict(),
            ChatResponseData(message=stream_response, messageType=MessageType.BOT_TEXT).dict()
        ]
        for msg in normal_ressponse:
            save_history.append(msg)
        await ChatService.save_history(user_id, save_history)