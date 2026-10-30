from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId
from backend.lib.db import db

router = APIRouter()

class MaintenanceRequestCreate(BaseModel):
    machine_id: str
    machine_name: str
    line_name: str
    issue_description: str
    operator_name: str
    priority: Optional[str] = "normal"

class StatusUpdate(BaseModel):
    status: str
    technician_name: Optional[str] = None
    notes: Optional[str] = None

@router.get("/requests")
async def get_all_requests(status: Optional[str] = None):
    query = {}
    if status:
        query["status"] = status

    cursor = db.requests.find(query).sort("created_at", -1)
    requests = []
    async for req in cursor:
        req["_id"] = str(req["_id"])
        requests.append(req)
    return {"ok": True, "data": requests}

@router.post("/requests")
async def create_request(req: MaintenanceRequestCreate):
    data = req.dict()
    data["status"] = "pending"
    data["created_at"] = datetime.utcnow().isoformat()

    res = await db.requests.insert_one(data)
    data["_id"] = str(res.inserted_id)
    return {"ok": True, "data": data}

@router.patch("/requests/{request_id}")
async def update_request_status(request_id: str, update: StatusUpdate):
    try:
        obj_id = ObjectId(request_id)
    except Exception:
        raise HTTPException(status_code=400, detail="معرف الطلب غير صالح")

    update_data = {k: v for k, v in update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow().isoformat()

    res = await db.requests.update_one({"_id": obj_id}, {"$set": update_data})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")

    return {"ok": True, "message": "تم تحديث حالة الطلب بنجاح"}
