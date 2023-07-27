from fastapi import APIRouter, Depends, HTTPException, status
from dtos.chatbot import ChatInput
from chatbot import chatbot

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])

@router.post("/layer-1")
async def chat_1(input: ChatInput):
    response = await chatbot.chat_layer_1(question=input.text, chat_history=input.chat_history)
    return response

@router.post("/layer-2")
async def chat_1(input: ChatInput):
    response = await chatbot.chat_layer_2_async_wrapper(question=input.text, chat_history=input.chat_history)
    return response