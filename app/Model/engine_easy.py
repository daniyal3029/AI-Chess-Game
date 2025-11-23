# app/model/engine_easy.py
# Easy engine: random move with preference for captures (Level 1)
# Strategy: 70% random, 30% best capture by material value

import random
import chess

# Piece values for material evaluation
vals = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def pick(board):
    """
    Level 1 Easy Engine: Rule-based with simple heuristics
    
    Args:
        board: chess.Board instance
        
    Returns:
        chess.Move or None if no legal moves
        
    Strategy:
        - 70% of the time: choose random legal move
        - 30% of the time: choose best capture (highest material gain)
        - If no captures available, choose random move
    """
    moves = list(board.legal_moves)
    if not moves:
        return None

    # Collect capture moves with material value
    captures = []
    for move in moves:
        if board.is_capture(move):
            target = board.piece_at(move.to_square)
            if target is None:
                # En passant capture, value as pawn
                score = vals[chess.PAWN]
            else:
                score = vals.get(target.piece_type, 0)
            captures.append((score, move))

    # 30% chance to choose best capture if available
    if captures and random.random() < 0.3:
        captures.sort(reverse=True, key=lambda x: x[0])
        return captures[0][1]

    # Otherwise random move (70% of the time or if no captures)
    return random.choice(moves)
