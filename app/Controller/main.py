# app/controller/main.py
# Main controller: glue between model and view, picks engine by difficulty.

import time
import chess
from app.Model.game import Game
from app.Model import engine_easy, engine_med, engine_hard
from app.Model.learning import LearningMemory
from app.View import terminal_ui

# Initialize memory
memory = LearningMemory()

def ai_move_for_level(level, board, hard_inst=None):
    # 1. Try learned move first (for all levels)
    learned_move = memory.get_best_move(board)
    if learned_move:
        return learned_move

    # 2. Fallback to engines
    if level == 1:
        return engine_easy.pick(board)
    if level == 2:
        return engine_med.best_move(board, depth=3)
    if level == 3:
        if hard_inst is None:
            hard_inst = engine_hard.HardEngine()
        return hard_inst.pick(board)
    return engine_easy.pick(board)

def play_gui():
    g = Game()
    hard = engine_hard.HardEngine()
    
    def ai_func(level, board):
        return ai_move_for_level(level, board, hard_inst=hard)
    
    # Trigger learning and history at game end
    def on_game_end(game_instance):
        # 1. Learning
        moves = []
        temp_board = chess.Board()
        for move in game_instance.b.move_stack:
            moves.append((temp_board.fen(), move.uci()))
            temp_board.push(move)
            
        result = game_instance.result()
        winner = None
        if result == "1-0":
            winner = chess.WHITE
        elif result == "0-1":
            winner = chess.BLACK
            
        if winner is not None:
            print(f"Game Over. Learning from winner: {result}")
            memory.learn_game(moves, winner)
            
        # 2. History
        # We need to access the history manager. It's in the GUI instance, 
        # but we can also instantiate one here or pass it.
        # Ideally, the GUI handles the history display, so the GUI should probably 
        # handle the saving too, or we do it here.
        # Let's do it here to keep logic separated, but we need the level.
        # The level is inside the closure of ai_func? No, it's passed to ai_func.
        # We don't have easy access to the level here unless we store it.
        # Actually, the GUI has the history manager. It's better if the GUI calls 
        # the save method directly or we pass the manager here.
        # But wait, the GUI already instantiates HistoryManager.
        # Let's let the GUI handle the saving since it knows the level.
        # I will update this callback to just do learning.
        pass

    from app.View.gui import InteractiveGui
    gui = InteractiveGui(g, ai_func, on_game_end_callback=on_game_end)
    gui.start()

if __name__ == "__main__":
    # Default to GUI
    play_gui()
