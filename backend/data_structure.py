from datetime import datetime, timedelta
from typing import Optional, List, Tuple
import uuid  
from pydantic import BaseModel, Field, ConfigDict

"""
   uuid is universal standard for generating session that is seraizliation ready
"""

class Song(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    title: str 
    artist: str 
    spotify_id: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None

    rating: int = Field(default=1000, ge=0) #'ge=0' ensures rating is Greater or Equal to 0
    wins: int = 0
    losses: int = 0


class Matchup(BaseModel):
    song_a: Song 
    song_b: Song
    round_number: int 
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    winner_id: Optional[str] = None
    

class Session(BaseModel):
    user_id: str 
    songs: List[Song] = Field(default_factory=list)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    current_round: int = 0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    matchups: List[Matchup] = Field(default_factory=list)
    current_matchup_index = int = 0

