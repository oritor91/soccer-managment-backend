from typing import List, Dict
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, field):
        schema.update(type="string")
        return schema


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
    id: PyObjectId = Field(alias="_id")
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class GameBase(BaseModel):
    """
    Base model for a game.
    """
    date: str
    time: str
    location: str
    players: List[Player] = []
    sorted_groups: Dict[str, List[Player]] = {}


class Game(GameBase):
    """
    Model for a game.
    Inherits from GameBase.
    """
    id: PyObjectId = Field(alias="_id")
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

