from typing import List
from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str
    phone_number: str
    position: str
    skill_level: int


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):

    @property
    def id(self):
        return f"{self.name}_{self.phone_number}"


class PlayerUpdateRequest(BaseModel):
    old: Player
    new: Player


class GameBase(BaseModel):
    date: str
    time: str
    location: str

class GameCreate(GameBase):
    player_ids: List[str] = []

class Game(GameBase):
    players: List[Player] = []
    
    @property
    def id(self):
        return f"{self.date}_{self.time}"

