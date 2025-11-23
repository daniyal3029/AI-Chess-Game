import json
import os
from datetime import datetime

HISTORY_FILE = "data/history.json"

class HistoryManager:
    def __init__(self):
        self.history = []
        self.load()

    def load(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
                self.history = []
        else:
            self.history = []

    def save_game(self, result, level, winner_color=None):
        """
        Save a completed game to history.
        result: str (e.g. "1-0", "0-1", "1/2-1/2")
        level: int (1, 2, 3)
        winner_color: chess.WHITE, chess.BLACK, or None
        """
        # Ensure data directory exists
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        level_str = "Easy"
        if level == 2: level_str = "Medium"
        if level == 3: level_str = "Hard"
        
        entry = {
            "timestamp": timestamp,
            "result": result,
            "level": level_str,
            "winner": "White" if winner_color == True else ("Black" if winner_color == False else "Draw")
        }
        
        self.history.insert(0, entry) # Add to beginning
        
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def get_history(self):
        return self.history
