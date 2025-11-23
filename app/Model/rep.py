# app/model/rep.py
# Board representation: Convert chess.Board to tensor format for neural networks

import numpy as np
import chess

# Piece mapping: 12 channels for 6 piece types × 2 colors
PIECE_MAP = {
    'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,  # White pieces
    'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11  # Black pieces
}

def board_to_tensor(b: chess.Board, include_metadata=True):
    """
    Convert a chess.Board to a tensor representation.
    
    Args:
        b: chess.Board instance
        include_metadata: If True, add side-to-move and castling rights planes
    
    Returns:
        numpy array of shape (8, 8, N) where N is 12, 13, or 17 depending on metadata
    """
    # Create 8x8x12 array for piece positions
    arr = np.zeros((8, 8, 12), dtype=np.float32)
    
    for sq, p in b.piece_map().items():
        # Convert square index to row, col
        # python-chess: 0=a1, 1=b1, ..., 63=h8
        r = 7 - (sq // 8)  # Row (0=rank8, 7=rank1)
        c = sq % 8          # Column (0=a-file, 7=h-file)
        ch = PIECE_MAP[p.symbol()]
        arr[r, c, ch] = 1.0
    
    if include_metadata:
        # Add side-to-move plane (1.0 if White to move, 0.0 if Black)
        stm = np.full((8, 8, 1), 1.0 if b.turn == chess.WHITE else 0.0, dtype=np.float32)
        arr = np.concatenate([arr, stm], axis=2)  # Shape becomes (8, 8, 13)
        
        # Optionally add castling rights (4 planes: white_kingside, white_queenside, black_kingside, black_queenside)
        castling = np.zeros((8, 8, 4), dtype=np.float32)
        if b.has_kingside_castling_rights(chess.WHITE):
            castling[:, :, 0] = 1.0
        if b.has_queenside_castling_rights(chess.WHITE):
            castling[:, :, 1] = 1.0
        if b.has_kingside_castling_rights(chess.BLACK):
            castling[:, :, 2] = 1.0
        if b.has_queenside_castling_rights(chess.BLACK):
            castling[:, :, 3] = 1.0
        arr = np.concatenate([arr, castling], axis=2)  # Shape becomes (8, 8, 17)
    
    return arr

def move_to_index(move: chess.Move, board: chess.Board = None):
    """
    Convert a chess.Move to a unique index.
    Simple implementation: use UCI string and map to index.
    
    For a full implementation, you'd want a consistent mapping of all 4672 possible moves.
    This is a simplified version that works for training.
    """
    uci = move.uci()
    # Simple hash-based index (not perfect but works for prototyping)
    # In production, use a proper move encoding like AlphaZero (from_square * 64 + to_square)
    from_sq = move.from_square
    to_sq = move.to_square
    promotion = move.promotion if move.promotion else 0
    # Encode: from_square (0-63) * 64 + to_square (0-63) + promotion_offset
    index = from_sq * 64 + to_sq + (promotion * 4096 if promotion else 0)
    return index

def index_to_move(index: int, board: chess.Board):
    """
    Convert an index back to a chess.Move.
    This is the inverse of move_to_index.
    """
    promotion = index // 4096
    remainder = index % 4096
    from_sq = remainder // 64
    to_sq = remainder % 64
    
    if promotion > 0:
        move = chess.Move(from_sq, to_sq, promotion=promotion)
    else:
        move = chess.Move(from_sq, to_sq)
    
    # Verify move is legal
    if move in board.legal_moves:
        return move
    return None

