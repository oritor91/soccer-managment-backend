from typing import List
from pydantic import BaseModel


class PlayerBase(BaseModel):
    """
    Base model for a player.
    """
    name: str
    phone_number: str
    position: str
    skill_level: int


class Player(PlayerBase):
    """
    Model for a player.
    Inherits from PlayerBase.
    """

    @property
    def id(self):
        """
        Returns the unique identifier for the player.
        """
        return f"{self.name}_{self.phone_number}"


class PlayerUpdateRequest(BaseModel):
    """
    Model for updating a player.
    """
    old: Player
    new: Player


class GameBase(BaseModel):
    """
    Base model for a game.
    """
    date: str
    time: str
    location: str


class Game(GameBase):
    """
    Model for a game.
    Inherits from GameBase.
    """
    players: List[Player] = []

    @property
    def id(self):
        """
        Returns the unique identifier for the game.
        """
        return f"{self.date}_{self.time}"

