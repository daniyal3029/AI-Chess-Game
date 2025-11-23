# app/model/engine_hard.py
# Hard engine: uses a TensorFlow/Keras evaluator if available to pick best 1-ply,
# otherwise falls back to medium engine.

import os
import chess
import numpy as np

# try to import tensorflow; if not present, we'll fall back
try:
    import tensorflow as tf
    TF_OK = True
except Exception:
    TF_OK = False

from . import engine_med

# small board -> tensor converter (same convention used for training later)
_piece_map = {
    'P':0,'N':1,'B':2,'R':3,'Q':4,'K':5,
    'p':6,'n':7,'b':8,'r':9,'q':10,'k':11
}

def board_to_tensor(b: chess.Board):
    # shape (8,8,12)
    arr = np.zeros((8,8,12), dtype=np.float32)
    for sq, p in b.piece_map().items():
        r = 7 - (sq // 8)
        c = sq % 8
        ch = _piece_map[p.symbol()]
        arr[r, c, ch] = 1.0
    # add side-to-move plane as extra channel
    stm = np.full((8,8,1), 1.0 if b.turn == chess.WHITE else 0.0, dtype=np.float32)
    out = np.concatenate([arr, stm], axis=2)  # shape (8,8,13)
    out = np.expand_dims(out, axis=0)  # batch dim
    return out

class HardEngine:
    def __init__(self, model_path="models/policy_eval.h5"):
        self.model = None
        if TF_OK and os.path.exists(model_path):
            try:
                self.model = tf.keras.models.load_model(model_path)
                print("HardEngine: loaded model", model_path)
            except Exception as e:
                print("HardEngine: failed to load model:", e)
                self.model = None
        else:
            if not TF_OK:
                print("HardEngine: tensorflow not available, falling back")
            else:
                print("HardEngine: no model file found, falling back")

    def pick(self, board: chess.Board):
        # If model available: evaluate each child board and pick best for current side
        if self.model is not None:
            best = None
            best_v = -1e9
            is_white = board.turn == chess.WHITE
            for m in board.legal_moves:
                board.push(m)
                x = board_to_tensor(board)
                try:
                    pred = self.model.predict(x, verbose=0)
                except Exception:
                    pred = None
                board.pop()
                if pred is None:
                    return engine_med.best_move(board, depth=3)
                # assume model outputs single scalar eval (higher = better for White)
                # if model outputs vector, take first scalar
                v = float(pred[0][0]) if pred.shape[-1] == 1 else float(pred[0].mean())
                # if playing black, invert value
                if not is_white:
                    v = -v
                if v > best_v:
                    best_v = v
                    best = m
            if best is None:
                return engine_med.best_move(board, depth=3)
            return best
        # fallback
        return engine_med.best_move(board, depth=3)
