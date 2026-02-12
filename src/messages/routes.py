from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from auth.dependencies import get_current_user
from llm.client import generate_stream
from db.client import supabase  # ✅ make sure this exists
import json
import uuid
import time

router = APIRouter()


class MessageRequest(BaseModel):
    content: str


@router.post("/{conversation_id}/messages/stream")
def stream_message(
    conversation_id: str,
    body: MessageRequest,
    user=Depends(get_current_user),
):

    # ✅ 1️⃣ SAVE USER MESSAGE BEFORE STREAMING
    supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": "user",
        "content": body.content,
        "token_count": len(body.content.split())
    }).execute()

    def event_generator():

        message_id = f"msg_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        full_response = ""
        finish_reason = "end_turn"

        # ✅ 2️⃣ message_start
        yield {
            "event": "message_start",
            "data": json.dumps({
                "type": "message_start",
                "message": {
                    "id": message_id,
                    "role": "assistant",
                    "model": "llama-3.1-8b-instant"
                }
            })
        }

        messages = [
            {"role": "user", "content": body.content}
        ]

        try:
            # ✅ 3️⃣ STREAM TOKENS
            for token in generate_stream(messages):
                full_response += token

                yield {
                    "event": "content_block_delta",
                    "data": json.dumps({
                        "type": "content_block_delta",
                        "index": 0,
                        "delta": {
                            "type": "text_delta",
                            "text": token
                        }
                    })
                }

            latency = int((time.time() - start_time) * 1000)
            output_tokens = len(full_response.split())

            # ✅ 4️⃣ SAVE ASSISTANT MESSAGE AFTER STREAM FINISHES
            supabase.table("messages").insert({
                "conversation_id": conversation_id,
                "role": "assistant",
                "content": full_response,
                "token_count": output_tokens,
            }).execute()

            # ✅ 5️⃣ message_delta (with usage + finish_reason)
            yield {
                "event": "message_delta",
                "data": json.dumps({
                    "type": "message_delta",
                    "delta": {
                        "stop_reason": finish_reason
                    },
                    "usage": {
                        "output_tokens": output_tokens
                    },
                    "latency_ms": latency
                })
            }

            yield {
                "event": "message_stop",
                "data": json.dumps({
                    "type": "message_stop"
                })
            }

        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({
                    "type": "error",
                    "error": {
                        "type": "model_error",
                        "message": str(e)
                    }
                })
            }

    return EventSourceResponse(event_generator())
