from typing import Literal, List
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatCommandData(BaseModel):
    user_id: str
    channel_id: str
    message: ChatMessage