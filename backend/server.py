from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, ops, admin

app = FastAPI(
    title="FixTrack API",
    version="3.0.0",
    description="Machine maintenance requests tracking system API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(ops.router, prefix="/api", tags=["Operations & Requests"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin & Stats"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "system": "FixTrack API is running"}
