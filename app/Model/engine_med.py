# app/model/engine_med.py
# Medium engine: Minimax with alpha-beta pruning (Level 2)
# Features: transposition table, move ordering, iterative deepening option

import chess
import math
import random
from typing import Optional, Dict, Tuple

# Piece values for material evaluation
VAL = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

# Transposition table: maps FEN -> (depth, score)
_transposition_table: Dict[str, Tuple[int, float]] = {}
_table_hits = 0

def clear_transposition_table():
    """Clear the transposition table (useful for new games)"""
    global _transposition_table, _table_hits
    _transposition_table.clear()
    _table_hits = 0

def eval_board(b: chess.Board) -> float:
    """
    Evaluation function: material + mobility + piece-square bonuses
    
    Args:
        b: chess.Board instance
        
    Returns:
        Evaluation score (positive = good for White, negative = good for Black)
    """
    score = 0.0
    
    # Material evaluation
    for square, piece in b.piece_map().items():
        piece_value = VAL.get(piece.piece_type, 0)
        if piece.color == chess.WHITE:
            score += piece_value
        else:
            score -= piece_value
    
    # Mobility bonus (number of legal moves)
    try:
        mobility = len(list(b.legal_moves))
        if b.turn == chess.WHITE:
            score += 0.01 * mobility
        else:
            score -= 0.01 * mobility
    except Exception:
        pass
    
    # Game over check
    if b.is_checkmate():
        if b.turn == chess.WHITE:
            return -1000.0  # Black wins
        else:
            return 1000.0   # White wins
    elif b.is_stalemate() or b.is_insufficient_material() or b.is_seventyfive_moves() or b.is_fivefold_repetition():
        return 0.0  # Draw
    
    return score

def negamax(b: chess.Board, depth: int, alpha: float, beta: float, color: int) -> float:
    """
    Negamax algorithm with alpha-beta pruning and transposition table
    
    Args:
        b: chess.Board instance
        depth: remaining search depth
        alpha: alpha value for pruning
        beta: beta value for pruning
        color: 1 if maximizing for White, -1 if maximizing for Black
        
    Returns:
        Best evaluation score from current position
    """
    global _transposition_table, _table_hits
    
    # Check transposition table
    fen = b.fen()
    if fen in _transposition_table:
        stored_depth, stored_score = _transposition_table[fen]
        if stored_depth >= depth:
            _table_hits += 1
            return stored_score
    
    # Terminal node
    if depth == 0 or b.is_game_over():
        eval_score = eval_board(b)
        result = color * eval_score
        _transposition_table[fen] = (0, result)
        return result
    
    # Generate and order moves (captures first)
    moves = list(b.legal_moves)
    moves.sort(key=lambda m: (
        0 if not b.is_capture(m) else 1,  # Captures first
        -VAL.get(b.piece_at(m.to_square).piece_type, 0) if b.is_capture(m) and b.piece_at(m.to_square) else 0
    ), reverse=True)
    
    max_value = -math.inf
    for move in moves:
        b.push(move)
        try:
            value = -negamax(b, depth - 1, -beta, -alpha, -color)
        finally:
            b.pop()
        
        if value > max_value:
            max_value = value
        
        if max_value > alpha:
            alpha = max_value
        
        # Alpha-beta cutoff
        if alpha >= beta:
            break
    
    # Store in transposition table
    _transposition_table[fen] = (depth, max_value)
    return max_value

def best_move(board: chess.Board, depth: int = 3) -> Optional[chess.Move]:
    """
    Level 2 Medium Engine: Minimax with alpha-beta pruning
    
    Args:
        board: chess.Board instance
        depth: search depth (default 3, can be 4 for stronger play)
        
    Returns:
        Best move according to minimax search, or None if no legal moves
    """
    moves = list(board.legal_moves)
    if not moves:
        return None
    
    best_move_found = None
    best_value = -math.inf
    root_color = 1 if board.turn == chess.WHITE else -1
    
    # Order moves: captures first
    moves.sort(key=lambda m: (
        0 if not board.is_capture(m) else 1,
        -VAL.get(board.piece_at(m.to_square).piece_type, 0) if board.is_capture(m) and board.piece_at(m.to_square) else 0
    ), reverse=True)
    
    # Search each move
    for move in moves:
        board.push(move)
        try:
            value = -negamax(board, depth - 1, -math.inf, math.inf, -root_color)
        except Exception as e:
            print(f"Error in negamax: {e}")
            value = -math.inf
        board.pop()
        
        if value > best_value:
            best_value = value
            best_move_found = move
        elif value == best_value and random.random() < 0.1:
             best_move_found = move

    if best_move_found is None:
        # Fallback to random legal move if something went wrong
        print("Warning: Minimax returned None, falling back to random")
        return random.choice(moves)

    return best_move_found
