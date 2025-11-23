import json
import os
import chess

DATA_FILE = "data/memory.json"

class LearningMemory:
    def __init__(self):
        self.memory = {}
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    self.memory = json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
                self.memory = {}
        else:
            self.memory = {}

    def save(self):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def learn_game(self, game_moves, winner_color):
        """
        Learn from a completed game.
        game_moves: List of (fen, move_uci) tuples
        winner_color: chess.WHITE or chess.BLACK
        """
        # We only want to learn moves played by the winner
        # Moves list should be in order. 
        # If White won, we learn White's moves (indices 0, 2, 4...)
        # If Black won, we learn Black's moves (indices 1, 3, 5...)
        
        start_index = 0 if winner_color == chess.WHITE else 1
        
        for i in range(start_index, len(game_moves), 2):
            fen, move_uci = game_moves[i]
            
            # Simplify FEN to just piece placement and turn to avoid over-specificity
            # (e.g. ignore halfmove clock, maybe castling rights if we want to be strict)
            # For now, let's use the full FEN but maybe strip the move counters
            key = fen.split(' ')[0] + ' ' + fen.split(' ')[1] 
            
            if key not in self.memory:
                self.memory[key] = {}
            
            if move_uci not in self.memory[key]:
                self.memory[key][move_uci] = 0
            
            self.memory[key][move_uci] += 1
            
        self.save()

    def get_best_move(self, board):
        """
        Return a learned move for the current board state if it exists.
        """
        fen = board.fen()
        key = fen.split(' ')[0] + ' ' + fen.split(' ')[1]
        
        if key in self.memory:
            moves = self.memory[key]
            if not moves:
                return None
            
            # Pick the move with the highest count
            # We could add randomness here to avoid being too predictable
            best_move_uci = max(moves, key=moves.get)
            
            # Verify legality
            try:
                move = chess.Move.from_uci(best_move_uci)
                if move in board.legal_moves:
                    print(f"Learning: Found learned move {best_move_uci} (count: {moves[best_move_uci]})")
                    return move
            except:
                pass
                
        return None
