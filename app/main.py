from fastapi import FastAPI
from datetime import date

from app.schemas import AITurnRequest, TurnPhase
from app.logic import choose_setup, choose_turn

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
    if body.turn_phase == TurnPhase.SETUP:
        return choose_setup(body.board)
    else:
        jogada = choose_turn(body.board, int(body.your_team))
        return jogada