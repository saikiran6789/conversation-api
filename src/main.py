from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from conversations.routes import router as convo_router
from messages.routes import router as message_router

app = FastAPI(title="AI Conversation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(convo_router, prefix="/api/v1/conversations", tags=["Conversations"])
app.include_router(message_router, prefix="/api/v1/conversations", tags=["Messages"])

@app.get("/")
def health():
    return {"status": "API running"}
