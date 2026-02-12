from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from db.client import supabase
from .password import hash_password, verify_password
from .jwt import create_access_token

router = APIRouter()

class AuthRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(data: AuthRequest):
    # Check if user exists
    existing = supabase.table("users").select("*").eq("email", data.email).execute()

    if existing.data:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(data.password)

    res = supabase.table("users").insert({
        "email": data.email,
        "password_hash": hashed
    }).execute()

    user = res.data[0]

    token = create_access_token({"sub": user["id"]})

    return {"access_token": token}


@router.post("/login")
def login(data: AuthRequest):

    res = supabase.table("users").select("*").eq("email", data.email).execute()

    if not res.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = res.data[0]

    if not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["id"]})

    return {"access_token": token}
