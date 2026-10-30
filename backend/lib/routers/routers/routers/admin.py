from fastapi import APIRouter
from backend.lib.db import db

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats():
    total_requests = await db.requests.count_documents({})
    pending = await db.requests.count_documents({"status": "pending"})
    in_progress = await db.requests.count_documents({"status": "in_progress"})
    completed = await db.requests.count_documents({"status": "completed"})

    return {
        "ok": True,
        "stats": {
            "total": total_requests,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed
        }
    }
