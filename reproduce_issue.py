import chess
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from app.Model import engine_med

def test_engine():
    board = chess.Board()
    print("Testing Medium Engine on starting board...")
    try:
        move = engine_med.best_move(board, depth=3)
        print(f"Move found: {move}")
    except Exception as e:
        print(f"ERROR caught in test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_engine()
