from app.schemas import Cell, SetupResponse, PlayerTurnResponse, Position
from typing import Optional
import random
import copy

BOARD_SIZE = 5
TEAM_PROFESSORS = {1: ["CLARO", "REY"], 2: ["KARIN", "BEATRIZ"]}
INF = float("inf")
SEARCH_DEPTH = 2

def board_to_dict(board: list) -> list:

    result = []
    for row in board:
        new_row = []
        for cell in row:
            if isinstance(cell, Cell):
                new_row.append({"level": cell.level, "professor": cell.professor})
            else:
                new_row.append(cell)
        result.append(new_row)
    return result


def move_to_response(move: dict):
    if "mentor_at" in move:
        return PlayerTurnResponse(
            professor=move["professor"],
            move_to=Position(row=move["move_to"]["row"], col=move["move_to"]["col"]),
            mentor_at=Position(row=move["mentor_at"]["row"], col=move["mentor_at"]["col"]),
        )
    return PlayerTurnResponse(
        professor=move["professor"],
        move_to=Position(row=move["move_to"]["row"], col=move["move_to"]["col"]),
    )

def escolher_jogada(board, your_team, turn_phase, professor_to_place):
    board = board_to_dict(board)

    if turn_phase == "setup_placement":
        return escolher_setup(board, professor_to_place)

    moves = gerar_jogadas(board, your_team)
    if not moves:
        raise RuntimeError("Nenhuma jogada válida encontrada")

    best_move = None
    best_score = -INF

    for move in moves:
        new_board = aplicar_jogada(board, move)
        score = minimax(new_board, SEARCH_DEPTH - 1, -INF, INF, False, your_team)
        if score > best_score:
            best_score = score
            best_move = move

    return move_to_response(best_move)

def escolher_setup(board: list, professor_to_place: Optional[str]) -> SetupResponse:
    candidates = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            cell = board[r][c]
            if cell["level"] == 0 and cell["professor"] is None:
                dist = abs(r - 2) + abs(c - 2)
                candidates.append((dist, r, c))

    if not candidates:
        raise RuntimeError("Sem célula válida para setup")

    candidates.sort()
    best_dist = candidates[0][0]
    top = [(r, c) for d, r, c in candidates if d == best_dist]
    r, c = random.choice(top)
    return SetupResponse(row=r, col=c)


def minimax(board, depth, alpha, beta, is_maximizing, my_team):
    opponent = 2 if my_team == 1 else 1
    current_team = my_team if is_maximizing else opponent

    terminal = check_terminal(board, my_team, opponent)
    if terminal is not None:
        return terminal

    if depth == 0:
        return heuristica(board, my_team, opponent)

    moves = gerar_jogadas(board, current_team)
    if not moves:
        return -INF if is_maximizing else INF

    if is_maximizing:
        value = -INF
        for move in moves:
            new_board = aplicar_jogada(board, move)
            value = max(value, minimax(new_board, depth - 1, alpha, beta, False, my_team))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = INF
        for move in moves:
            new_board = aplicar_jogada(board, move)
            value = min(value, minimax(new_board, depth - 1, alpha, beta, True, my_team))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def check_terminal(board, my_team, opponent):
    for team, score in [(my_team, INF), (opponent, -INF)]:
        for prof in TEAM_PROFESSORS[team]:
            pos = find_professor(board, prof)
            if pos and board[pos[0]][pos[1]]["level"] == 3:
                return score
    return None


def heuristica(board, my_team, opponent):
    score = 0

    W_MY_LEVEL = 4
    W_MY_ADJ2  = 3
    W_OPP_ADJ2 = 3
    W_CENTER   = 1
    W_THREAT   = 30

    for team, sign in [(my_team, 1), (opponent, -1)]:
        for prof in TEAM_PROFESSORS[team]:
            pos = find_professor(board, prof)
            if pos is None:
                continue
            r, c = pos
            cur_level = board[r][c]["level"]

            score += sign * W_MY_LEVEL * cur_level

            adj2_count = 0
            for nr, nc in adjacent_cells(r, c):
                cell = board[nr][nc]
                if cell["professor"] is None and cell["level"] < 4:
                    if cell["level"] <= cur_level + 1 and cell["level"] == 2:
                        adj2_count += 1

            score += sign * (W_MY_ADJ2 if sign == 1 else W_OPP_ADJ2) * adj2_count

            dist_center = abs(r - 2) + abs(c - 2)
            score += sign * W_CENTER * (4 - dist_center)

    for team, sign in [(opponent, -1), (my_team, 1)]:
        for prof in TEAM_PROFESSORS[team]:
            pos = find_professor(board, prof)
            if pos is None:
                continue
            r, c = pos
            cur_level = board[r][c]["level"]
            for nr, nc in adjacent_cells(r, c):
                cell = board[nr][nc]
                if (
                    cell["professor"] is None
                    and cell["level"] == 3
                    and cell["level"] <= cur_level + 1
                ):
                    score += sign * W_THREAT

    return score


def gerar_jogadas(board, team_id):
    winning_moves   = []
    candidate_moves = []

    for professor in TEAM_PROFESSORS[team_id]:
        pos = find_professor(board, professor)
        if pos is None:
            continue
        cur_row, cur_col = pos
        cur_level = board[cur_row][cur_col]["level"]

        for dst_row, dst_col in adjacent_cells(cur_row, cur_col):
            dst = board[dst_row][dst_col]
            if dst["professor"] is not None:
                continue
            if dst["level"] == 4:
                continue
            if dst["level"] > cur_level + 1:
                continue

            if dst["level"] == 3:
                winning_moves.append({
                    "professor": professor,
                    "move_to": {"row": dst_row, "col": dst_col},
                })
                continue

            for men_row, men_col in adjacent_cells(dst_row, dst_col):
                men = board[men_row][men_col]
                source_cell = (men_row, men_col) == (cur_row, cur_col)
                if (men["professor"] is None or source_cell) and men["level"] < 4:
                    candidate_moves.append({
                        "professor": professor,
                        "move_to":  {"row": dst_row, "col": dst_col},
                        "mentor_at": {"row": men_row, "col": men_col},
                    })

    return winning_moves + candidate_moves


def aplicar_jogada(board, move):
    new_board = [
    [cell.copy() for cell in row]
    for row in board
]
    professor = move["professor"]
    cur_row, cur_col = find_professor(new_board, professor)
    dst_row = move["move_to"]["row"]
    dst_col = move["move_to"]["col"]

    new_board[cur_row][cur_col]["professor"] = None
    new_board[dst_row][dst_col]["professor"] = professor

    if new_board[dst_row][dst_col]["level"] != 3 and "mentor_at" in move:
        men_row = move["mentor_at"]["row"]
        men_col = move["mentor_at"]["col"]
        new_board[men_row][men_col]["level"] = min(4, new_board[men_row][men_col]["level"] + 1)

    return new_board


def adjacent_cells(row, col):
    result = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                result.append((nr, nc))
    return result


def find_professor(board, name):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c]["professor"] == name:
                return (r, c)
    return None
