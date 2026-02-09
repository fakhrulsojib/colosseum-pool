from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class HeroImage(BaseModel):
    id: int
    url: str
    alt: str
    title: str
    subtitle: str

# Mock data for Pool - simulating DB fetch
pool_hero_images_data = [
    {
        "id": 1,
        "url": 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=1200&h=600&fit=crop',
        "alt": 'Pool Tournament Action',
        "title": 'Pool Championship',
        "subtitle": 'Watch the best compete for glory'
    },
    {
        "id": 2,
        "url": 'https://images.unsplash.com/photo-1534158914592-062992bbe900?w=1200&h=600&fit=crop',
        "alt": '8-Ball Showdown',
        "title": '8-Ball Showdown',
        "subtitle": 'Live from the Grand Arena'
    }
]

@router.get("/", response_model=List[HeroImage])
def get_hero_images():
    """
    Get list of hero images for the Pool landing page.
    """
    return pool_hero_images_data
