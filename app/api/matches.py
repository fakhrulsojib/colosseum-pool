from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import Match

router = APIRouter()

class MatchCreate(BaseModel):
    winner_id: int
    loser_id: int

class MatchResponse(BaseModel):
    id: int
    winner_id: int
    loser_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=MatchResponse)
async def create_match(match: MatchCreate, db: AsyncSession = Depends(get_db)):
    db_match = Match(
        winner_id=match.winner_id,
        loser_id=match.loser_id,
        timestamp=datetime.utcnow()
    )
    db.add(db_match)
    await db.commit()
    await db.refresh(db_match)
    return db_match

@router.get("/", response_model=List[MatchResponse])
async def get_matches(
    skip: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Match).order_by(desc(Match.timestamp)).offset(skip).limit(limit))
    return result.scalars().all()
