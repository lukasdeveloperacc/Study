from dotenv import load_dotenv
from fastapi import FastAPI
from openai import AsyncOpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
client = AsyncOpenAI()

class CreateConversationResponse(BaseModel):
    conversation_id: str

@app.post("/conversations")
async def create_conversation() -> CreateConversationResponse:
    conversation = await client.conversations.create()

    return CreateConversationResponse(conversation_id=conversation.id)    

@app.post("/conversations/{conversation_id}/message")
async def create_message(conversation_id: str, message: str) -> None:
    pass
