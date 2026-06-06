from enum import IntEnum, Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class TeamID(IntEnum):
    TURING = 1 #Claro e Rey
    LOVELACE = 2 #Karin e Bea

class TurnPhase(str, Enum):
    SETUP = "setup_placement"
    PLAYER_TURN = "player_turn"

class Cell(BaseModel):
    level: int = Field(ge=0, le=4)
    professor: Optional[str] = None

class Position(BaseModel):
    row: int = Field(ge=0, le=4)
    col : int = Field(ge=0, le=4)

class AITurnRequest(BaseModel):
    game_id: str
    turn_number: int
    turn_phase: str 
    your_team: int
    professor_to_place: Optional[str] = Field(default=None)
    board: List[List[Cell]]

class SetupResponse(BaseModel):
    row: int = Field(ge=0, le=4)
    col  : int = Field(ge=0, le=4)

class PlayerTurnResponse(BaseModel):
    professor: str
    move_to: Position
    mentor_at: Optional[Position] = None
