from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.conversation import (
    start_conversation,
    send_message,
    load_history,
    delete_conversation,
)

router = APIRouter(prefix="/agent", tags=["agent"])

USER_ID = 1  # single user for now


class MessageRequest(BaseModel):
    content: str


# --- Conversations ---

@router.post("/conversations")
def new_conversation():
    conversation_id = start_conversation(USER_ID)
    return {"conversation_id": conversation_id}


@router.get("/conversations/{conversation_id}/history")
def get_history(conversation_id: int):
    history = load_history(conversation_id)
    if not history:
        raise HTTPException(status_code=404, detail="Conversation not found or empty")
    return {"conversation_id": conversation_id, "messages": history}


@router.delete("/conversations/{conversation_id}")
def remove_conversation(conversation_id: int):
    delete_conversation(USER_ID, conversation_id)
    return {"deleted": conversation_id}


# --- Messaging ---

@router.post("/conversations/{conversation_id}/messages")
def chat(conversation_id: int, body: MessageRequest):
    reply = send_message(body.content, conversation_id)
    return {"role": "assistant", "content": reply}
