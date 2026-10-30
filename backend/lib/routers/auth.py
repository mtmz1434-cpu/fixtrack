from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from backend.lib.db import db

router = APIRouter()

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    role: str
    badge_number: Optional[str] = None

@router.post("/login")
async def login(credentials: UserLogin):
    user = await db.users.find_one({"username": credentials.username})
    if not user or user.get("password") != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة"
        )
    return {
        "ok": True,
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "name": user.get("name", user["username"]),
            "role": user.get("role", "operator"),
            "badge_number": user.get("badge_number", "")
        }
    }

@router.post("/register")
async def register(user_data: UserCreate):
    existing = await db.users.find_one({"username": user_data.username})
    if existing:
        raise HTTPException(status_code=400, detail="اسم المستخدم مسجل مسبقاً")

    new_user = user_data.dict()
    res = await db.users.insert_one(new_user)
    return {"ok": True, "id": str(res.inserted_id)}
