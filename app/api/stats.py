from fastapi import APIRouter

router = APIRouter()

@router.get("/leaderboard")
async def get_leaderboard():
    return {"message": "Leaderboard stats"}
