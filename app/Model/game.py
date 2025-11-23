# app/model/game.py
# Wrapper around python-chess Board to provide simple API for controller/view

import chess

class Game:
    def __init__(self):
        self.b = chess.Board()

    def reset(self):
        self.b.reset()

    def fen(self):
        return self.b.fen()

    def legal_moves(self):
        return list(self.b.legal_moves)

    def push_uci(self, uci):
        try:
            m = chess.Move.from_uci(uci)
        except Exception:
            return False, "bad-uci"
        if m in self.b.legal_moves:
            self.b.push(m)
            return True, None
        return False, "illegal"

    def push_san(self, san):
        try:
            m = self.b.parse_san(san)
        except Exception as e:
            return False, str(e)
        self.b.push(m)
        return True, None

    def push_move(self, move):
        # move: chess.Move
        if move in self.b.legal_moves:
            self.b.push(move)
            return True
        return False

    def pop(self):
        return self.b.pop()

    def is_over(self):
        return self.b.is_game_over()

    def result(self):
        return self.b.result()

    def turn(self):
        # True for White to move, False for Black
        return self.b.turn

    def unicode(self):
        # Return a pretty text board
        return self.b.unicode(invert_color=False)

    def san(self, move):
        return self.b.san(move)

    def copy_board(self):
        return self.b.copy()
