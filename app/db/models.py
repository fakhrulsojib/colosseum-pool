from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    winner_id = Column(Integer)
    loser_id = Column(Integer)
    timestamp = Column(DateTime)

class Stat(Base):
    __tablename__ = "stats"

    user_id = Column(Integer, primary_key=True)
    elo = Column(Integer, default=1200)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)

class HeroImage(Base):
    __tablename__ = "hero_images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)  # Text to support Base64 strings
    alt = Column(String, nullable=True)
    title = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
