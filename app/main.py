from fastapi import FastAPI
from app.api import matches, stats

app = FastAPI(title="Colosseum Pool", version="0.1.0")

app.include_router(matches.router, prefix="/api/pool/matches", tags=["matches"])
app.include_router(stats.router, prefix="/api/pool/stats", tags=["stats"])

@app.get("/")
async def root():
    return {"message": "Welcome to Colosseum Pool Game Engine"}
