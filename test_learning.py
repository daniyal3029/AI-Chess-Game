import chess
import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

from app.Model.learning import LearningMemory

def test_learning():
    print("Testing Learning System...")
    memory = LearningMemory()
    
    # Simulate a short game won by White
    # 1. e4 e5 2. Qh5 (Scholar's mate attempt)
    moves = [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4"),
        ("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1", "e7e5"),
        ("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2", "d1h5")
    ]
    
    print("Learning from White win...")
    memory.learn_game(moves, chess.WHITE)
    
    # Check if memory file exists
    if os.path.exists("data/memory.json"):
        print("Memory file created.")
        with open("data/memory.json", 'r') as f:
            data = json.load(f)
            print("Memory content:", json.dumps(data, indent=2))
            
            # Verify e2e4 is learned
            start_fen_key = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
            if start_fen_key in data and "e2e4" in data[start_fen_key]:
                print("SUCCESS: Learned e2e4 for start position.")
            else:
                print("FAILURE: Did not learn e2e4.")
    else:
        print("FAILURE: Memory file not created.")

    # Test retrieval
    board = chess.Board()
    best_move = memory.get_best_move(board)
    print(f"Best move for start pos: {best_move}")
    
    if best_move == chess.Move.from_uci("e2e4"):
        print("SUCCESS: Retrieved learned move correctly.")
    else:
        print(f"FAILURE: Retrieved {best_move}, expected e2e4")

if __name__ == "__main__":
    test_learning()
