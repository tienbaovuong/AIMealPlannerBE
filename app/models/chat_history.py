from typing import Union, List
from pymongo import ASCENDING, IndexModel

from app.models.base import RootModel, RootEnum

class MessageType(str, RootEnum):
    BOT_TEXT = "BOT_TEXT_MESSAGE"
    BOT_DETAIL = "BOT_DETAIL_MESSAGE"
    STREAM = "STREAM_MESSAGE"
    USER = "USERMESSAGE"
    SYSTEM = "SYSTEMMESSAGE"

class ChatHistory(RootModel):
    class Collection:
        name = "chat_history"
        indexes = [
            IndexModel(
                [
                    ("user_id", ASCENDING),
                ]
            )
        ]

    user_id: str
    messageType: MessageType
    message: Union[str, dict]