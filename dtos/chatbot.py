from pydantic import BaseModel

class ChatInput(BaseModel):
    text: str
    chat_history: list