from pydantic import BaseModel
from typing import Union

from app.dto.common import BaseResponseData
from app.models.chat_history import MessageType

class ChatResponseData(BaseModel):
    message: Union[str, dict]
    messageType: MessageType

class ChatResponse(BaseResponseData):
    data: ChatResponseData