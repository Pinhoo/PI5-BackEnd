from fastapi import FastAPI
from datetime import date

from app.schemas import AITurnRequest, TurnPhase
from app.logic import escolher_jogada

app = FastAPI(
    title="Sedento - By Gulosos",
    description="API para o PI5",
    version="0.0.1"
)

@app.get("/health")
async def health():
    return date.today()

@app.post("/move")
async def move(body: AITurnRequest):
    return escolher_jogada(board= body.board, your_team=body.your_team, turn_phase=body.turn_phase, professor_to_place=body.professor_to_place)
