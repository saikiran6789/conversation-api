**🧠 AI Conversation API — Secure Streaming Chat Backend**

A production-grade AI Conversation REST API built with FastAPI + Supabase + Groq (LLM) featuring:

**🔐 JWT Authentication**

**💬 Conversation CRUD**

**⚡ Real-time SSE streaming (token-by-token)**

**📊 Token usage tracking**

**🛡️ Row Level Security (RLS)**

**📘 Auto-generated Swagger Docs**

**🔒 Secure architecture**

**🚀 Tech Stack**
Component	Technology
Framework	FastAPI
Database	Supabase PostgreSQL
Auth	Custom JWT
LLM	Groq (Llama 3.1 8B Instant)
Streaming	Server-Sent Events (SSE)
Validation	Pydantic
Docs	Swagger (/docs)
**📂 Project Structure**
conversation-api/
│
├── src/
│   ├── main.py
│   ├── auth/
│   ├── conversations/
│   ├── messages/
│   ├── llm/
│   ├── db/
│   └── middleware/
│
├── database/schema.sql
├── requirements.txt
├── .env.example
└── README.md

**⚙️ Setup Instructions**
**1️⃣ Clone the repository**
git clone https://github.com/saikiran6789/conversation-api
cd conversation-api

**2️⃣ Create virtual environment**
python -m venv venv
venv\Scripts\activate   # Windows

**3️⃣ Install dependencies**
pip install -r requirements.txt

**4️⃣ Setup Environment Variables**

Create .env file:

JWT_SECRET=your_secure_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

GROQ_API_KEY=your_groq_api_key

**5️⃣ Run the server**
uvicorn main:app --reload --app-dir src


Server runs at:

http://127.0.0.1:8000


Swagger Docs:

http://127.0.0.1:8000/docs

**🔐 Authentication Flow**
Register

POST /api/v1/auth/register

Returns:

{
  "access_token": "..."
}

Login

POST /api/v1/auth/login

Returns new JWT token.

Use token in:

Authorization: Bearer <token>

**💬 Conversations**
Create Conversation

POST /api/v1/conversations

Returns:

{
  "id": "uuid-value"
}

List Conversations

GET /api/v1/conversations

**⚡ Streaming Messages**
Stream Endpoint
POST /api/v1/conversations/{conversation_id}/messages/stream


Streaming format follows SSE standard:

event: message_start
event: content_block_delta
event: message_delta
event: message_stop


✔ Token-by-token streaming
✔ Proper SSE format
✔ Error event handling
✔ Latency tracking
✔ Usage tracking

**📊 Token & Usage Tracking**

Each assistant message stores:

token_count

finish_reason

latency_ms

model

metadata

**🛡️ Security Features**

✅ JWT Authentication

✅ Supabase Row Level Security

✅ Authorization (users access only their data)

✅ Input validation (Pydantic)

✅ Secure password hashing (bcrypt)

✅ Environment variable secrets

✅ Structured error responses

🗄️ Database Schema

**Tables:**

users

conversations

messages

api_keys (optional)

See: database/schema.sql

**📡 Streaming Implementation**


Real-time token delivery

Proper SSE event format

Graceful error handling

Message persisted after stream completion

Token usage stored

Finish reason tracked
