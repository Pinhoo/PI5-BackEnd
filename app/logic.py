from app.schemas import Cell, SetupResponse
from typing import Optional
import random

def choose_setup(board: list[list[Cell]]) -> SetupResponse:
    candidates = [
        (r, c)
        for r in range(5)
        for c in range(5)
        if board[r][c].level == 0 and board[r][c].professor is None
    ]
    row, col = random.choice(candidates)
    return SetupResponse(row=1, col=0)

def choose_turn(board: list[list[Cell]]) -> SetupResponse:
    candidates = [
        (r, c)
        for r in range(5)
        for c in range(5)
        if board[r][c].level == 0 and board[r][c].professor is None
    ]
    row, col = random.choice(candidates)
    return SetupResponse(row=1, col=0)