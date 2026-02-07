from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    winner_id = Column(Integer) # ForeignKey to User in Core
    loser_id = Column(Integer)  # ForeignKey to User in Core
    timestamp = Column(DateTime)

class Stat(Base):
    __tablename__ = "stats"

    user_id = Column(Integer, primary_key=True)
    elo = Column(Integer, default=1200)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
