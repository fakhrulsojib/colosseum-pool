from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_match():
    return {"message": "Match created"}
