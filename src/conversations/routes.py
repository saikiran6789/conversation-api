from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user
from db.client import supabase
import uuid

router = APIRouter()

@router.post("")
def create_conversation(user=Depends(get_current_user)):

    conversation_id = str(uuid.uuid4())

    supabase.table("conversations").insert({
        "id": conversation_id,
        "user_id": user,
        "title": "New Chat",
        "model": "llama-3.1-8b-instant"
    }).execute()

    return {"id": conversation_id}


@router.get("")
def list_conversations(user=Depends(get_current_user)):
    return {k: v for k, v in fake_conversations.items() if v["user"] == user}
