from fastapi import APIRouter

start_router = APIRouter()

@start_router.get("/")
async def root():
    return {"message": "working"}