# app/View/gui.py
import tkinter as tk
from tkinter import messagebox
import chess
import threading
import time
from app.Model.history import HistoryManager

# --- Theme & Constants ---
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
PANEL_WIDTH = 250

# Colors
COLOR_LIGHT = "#E0E0E0"
COLOR_DARK = "#404040"
COLOR_BG = "#202020"
COLOR_TEXT = "#FFFFFF"
COLOR_BTN = "#606060"
COLOR_BTN_HOVER = "#808080"

# Highlights
COLOR_HIGHLIGHT_MOVES = "#87CEFA"
COLOR_HIGHLIGHT_CAPTURE = "#FF6347"
COLOR_HIGHLIGHT_SELECTED = "#FFD700"
COLOR_HIGHLIGHT_CHECK = "#8B0000"
COLOR_LAST_MOVE = "#FFFFE0"

PIECE_VALUES = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}

UNICODE_PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}

class InteractiveGui:
    def __init__(self, game, ai_func, on_game_end_callback=None):
        self.game = game
        self.ai_func = ai_func
        self.on_game_end_callback = on_game_end_callback
        self.history_manager = HistoryManager()
        
        self.root = tk.Tk()
        self.root.title("Chess AI - Master Edition")
        self.root.geometry(f"{BOARD_SIZE + PANEL_WIDTH}x{BOARD_SIZE}")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)

        # State
        self.selected_square = None
        self.game_over = False
        self.paused = False
        self.ai_thinking = False
        self.level = 2
        self.animating = False

        # UI Containers
        self.container = tk.Frame(self.root, bg=COLOR_BG)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.show_main_menu()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- Main Menu ---
    def show_main_menu(self):
        self.clear_container()
        
        frame = tk.Frame(self.container, bg=COLOR_BG)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        lbl_title = tk.Label(frame, text="CHESS AI", font=("Helvetica", 48, "bold"), bg=COLOR_BG, fg=COLOR_TEXT)
        lbl_title.pack(pady=(0, 40))

        lbl_sub = tk.Label(frame, text="Select Difficulty", font=("Helvetica", 16), bg=COLOR_BG, fg="#AAAAAA")
        lbl_sub.pack(pady=(0, 20))

        self.create_menu_btn(frame, "Easy (Random)", lambda: self.start_game(1))
        self.create_menu_btn(frame, "Medium (Minimax)", lambda: self.start_game(2))
        self.create_menu_btn(frame, "Hard (Neural Net)", lambda: self.start_game(3))
        
        tk.Label(frame, bg=COLOR_BG).pack(pady=10) # Spacer
        self.create_menu_btn(frame, "View History", self.show_history)

    def create_menu_btn(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=("Helvetica", 14), bg=COLOR_BTN, fg=COLOR_TEXT,
                        activebackground=COLOR_BTN_HOVER, activeforeground=COLOR_TEXT,
                        width=20, pady=10, relief=tk.FLAT, command=command)
        btn.pack(pady=5)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_BTN))

    # --- History View ---
    def show_history(self):
        self.clear_container()
        
        frame = tk.Frame(self.container, bg=COLOR_BG)
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        lbl = tk.Label(frame, text="Game History", font=("Helvetica", 24, "bold"), bg=COLOR_BG, fg=COLOR_TEXT)
        lbl.pack(pady=(0, 20))
        
        # Scrollable list
        list_frame = tk.Frame(frame, bg=COLOR_BG)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        lb = tk.Listbox(list_frame, font=("Courier", 12), bg="#303030", fg=COLOR_TEXT, 
                        yscrollcommand=scrollbar.set, relief=tk.FLAT, height=15)
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=lb.yview)
        
        history = self.history_manager.get_history()
        if not history:
            lb.insert(tk.END, "No games played yet.")
        else:
            lb.insert(tk.END, f"{'Date':<20} | {'Level':<10} | {'Result':<10} | {'Winner':<10}")
            lb.insert(tk.END, "-"*60)
            for entry in history:
                line = f"{entry['timestamp']:<20} | {entry['level']:<10} | {entry['result']:<10} | {entry['winner']:<10}"
                lb.insert(tk.END, line)
                
        btn_back = tk.Button(frame, text="Back to Menu", font=("Helvetica", 14), bg=COLOR_BTN, fg=COLOR_TEXT,
                             command=self.show_main_menu, relief=tk.FLAT)
        btn_back.pack(pady=20)

    # --- Game View ---
    def start_game(self, level):
        self.level = level
        self.game.reset()
        self.game_over = False
        self.paused = False
        self.selected_square = None
        self.ai_thinking = False
        self.animating = False
        
        self.clear_container()
        
        self.canvas = tk.Canvas(self.container, width=BOARD_SIZE, height=BOARD_SIZE, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self.on_click)

        self.panel = tk.Frame(self.container, width=PANEL_WIDTH, bg=COLOR_BG)
        self.panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.panel.pack_propagate(False)

        ctrl_frame = tk.Frame(self.panel, bg=COLOR_BG)
        ctrl_frame.pack(fill=tk.X, padx=20, pady=20)

        self.btn_pause = tk.Button(ctrl_frame, text="PAUSE", font=("Helvetica", 12, "bold"), 
                                   bg="#D32F2F", fg="white", relief=tk.FLAT, command=self.toggle_pause)
        self.btn_pause.pack(side=tk.LEFT)

        self.lbl_score = tk.Label(ctrl_frame, text="Score: 0", font=("Helvetica", 14, "bold"), bg=COLOR_BG, fg=COLOR_TEXT)
        self.lbl_score.pack(side=tk.RIGHT)

        self.lbl_status = tk.Label(self.panel, text="White to move", font=("Helvetica", 14), bg=COLOR_BG, fg="#AAAAAA", wraplength=PANEL_WIDTH-20)
        self.lbl_status.pack(pady=20)

        self.pause_menu = tk.Frame(self.container, bg=COLOR_BG, bd=2, relief=tk.RAISED)
        self.game_over_window = tk.Frame(self.container, bg=COLOR_BG, bd=2, relief=tk.RAISED)
        
        self.draw_board()
        self.update_score()

    def draw_board(self, exclude_square=None):
        self.canvas.delete("all")
        board = self.game.b
        
        # Squares
        for r in range(8):
            for c in range(8):
                color = COLOR_LIGHT if (r + c) % 2 == 0 else COLOR_DARK
                x1, y1 = c * SQUARE_SIZE, r * SQUARE_SIZE
                x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
                
                if board.move_stack:
                    last = board.peek()
                    if chess.square(c, 7-r) in [last.from_square, last.to_square]:
                         color = "#F0F0D0" if (r+c)%2 == 0 else "#606040"

                piece = board.piece_at(chess.square(c, 7-r))
                if piece and piece.piece_type == chess.KING and piece.color == board.turn and board.is_check():
                    color = COLOR_HIGHLIGHT_CHECK

                if self.selected_square == chess.square(c, 7-r):
                    color = COLOR_HIGHLIGHT_SELECTED

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # Legal Moves
        if self.selected_square is not None:
            piece = board.piece_at(self.selected_square)
            if piece:
                for move in board.legal_moves:
                    if move.from_square == self.selected_square:
                        tc, tr = chess.square_file(move.to_square), 7 - chess.square_rank(move.to_square)
                        tx1, ty1 = tc * SQUARE_SIZE, tr * SQUARE_SIZE
                        tx2, ty2 = tx1 + SQUARE_SIZE, ty1 + SQUARE_SIZE
                        
                        if board.is_capture(move) or board.is_en_passant(move):
                            self.canvas.create_rectangle(tx1+5, ty1+5, tx2-5, ty2-5, outline=COLOR_HIGHLIGHT_CAPTURE, width=4)
                        else:
                            cx, cy = (tx1+tx2)/2, (ty1+ty2)/2
                            self.canvas.create_oval(cx-10, cy-10, cx+10, cy+10, fill=COLOR_HIGHLIGHT_MOVES, outline="")

        # Pieces
        for sq, piece in board.piece_map().items():
            if exclude_square == sq: continue # Skip drawing piece being animated
            
            c, r = chess.square_file(sq), 7 - chess.square_rank(sq)
            x, y = c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2
            
            txt = UNICODE_PIECES[piece.symbol()]
            color = "white" if piece.color == chess.WHITE else "black"
            self.canvas.create_text(x+1, y+1, text=txt, font=("Arial", 40), fill="gray")
            self.canvas.create_text(x, y, text=txt, font=("Arial", 40), fill=color)

    def animate_move(self, move, callback):
        self.animating = True
        board = self.game.b
        piece = board.piece_at(move.from_square)
        if not piece: # Should not happen
            callback()
            return

        start_c, start_r = chess.square_file(move.from_square), 7 - chess.square_rank(move.from_square)
        end_c, end_r = chess.square_file(move.to_square), 7 - chess.square_rank(move.to_square)
        
        start_x = start_c * SQUARE_SIZE + SQUARE_SIZE // 2
        start_y = start_r * SQUARE_SIZE + SQUARE_SIZE // 2
        end_x = end_c * SQUARE_SIZE + SQUARE_SIZE // 2
        end_y = end_r * SQUARE_SIZE + SQUARE_SIZE // 2
        
        # Draw board without the moving piece
        self.draw_board(exclude_square=move.from_square)
        
        # Create animated piece
        txt = UNICODE_PIECES[piece.symbol()]
        color = "white" if piece.color == chess.WHITE else "black"
        shadow_item = self.canvas.create_text(start_x+1, start_y+1, text=txt, font=("Arial", 40), fill="gray")
        piece_item = self.canvas.create_text(start_x, start_y, text=txt, font=("Arial", 40), fill=color)
        
        steps = 10
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        
        def step(i):
            if i < steps:
                self.canvas.move(shadow_item, dx, dy)
                self.canvas.move(piece_item, dx, dy)
                self.root.after(15, lambda: step(i+1))
            else:
                self.canvas.delete(shadow_item)
                self.canvas.delete(piece_item)
                self.animating = False
                callback()

        step(0)

    def make_move(self, move):
        # Animate first, then push move
        self.animate_move(move, lambda: self.finalize_human_move(move))

    def finalize_human_move(self, move):
        self.game.push_move(move)
        self.selected_square = None
        self.update_score()
        self.draw_board()
        self.check_game_over()
        
        if not self.game_over:
            self.ai_thinking = True
            self.lbl_status.config(text="AI is thinking...", fg="#4FC3F7")
            self.root.update()
            threading.Thread(target=self.run_ai, daemon=True).start()

    def run_ai(self):
        try:
            time.sleep(0.5)
            while self.paused: time.sleep(0.1)
            move = self.ai_func(self.level, self.game.copy_board())
            self.root.after(0, lambda: self.start_ai_animation(move))
        except Exception as e:
            print(f"AI Error: {e}")
            self.ai_thinking = False
            self.lbl_status.config(text="AI Error", fg="red")

    def start_ai_animation(self, move):
        if self.game_over: return
        if move:
            self.animate_move(move, lambda: self.finalize_ai_move(move))
        else:
            self.ai_thinking = False
            self.check_game_over()

    def finalize_ai_move(self, move):
        self.game.push_move(move)
        self.update_score()
        self.draw_board()
        self.lbl_status.config(text="Your turn", fg="#AAAAAA")
        self.ai_thinking = False
        self.check_game_over()

    def check_game_over(self):
        if self.game.is_over():
            self.game_over = True
            result = self.game.result()
            self.show_game_over_window(result)
            
            # Save History
            winner_color = None
            if result == "1-0": winner_color = True
            elif result == "0-1": winner_color = False
            self.history_manager.save_game(result, self.level, winner_color)
            
            if self.on_game_end_callback:
                self.on_game_end_callback(self.game)

    def show_game_over_window(self, result):
        self.game_over_window.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=300)
        for w in self.game_over_window.winfo_children(): w.destroy()
        
        msg = "Game Over"
        if result == "1-0": msg = "White Wins!"
        elif result == "0-1": msg = "Black Wins!"
        elif result == "1/2-1/2": msg = "Draw!"
        
        tk.Label(self.game_over_window, text=msg, font=("Helvetica", 24, "bold"), bg=COLOR_BG, fg=COLOR_HIGHLIGHT_SELECTED).pack(pady=30)
        tk.Label(self.game_over_window, text=f"Result: {result}", font=("Helvetica", 18), bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=10)
        
        tk.Button(self.game_over_window, text="Back to Menu", command=self.show_main_menu, 
                  bg=COLOR_BTN, fg=COLOR_TEXT, font=("Helvetica", 14), width=15).pack(pady=30)

    def update_score(self):
        w_mat = sum(PIECE_VALUES.get(p.piece_type, 0) for p in self.game.b.piece_map().values() if p.color == chess.WHITE)
        b_mat = sum(PIECE_VALUES.get(p.piece_type, 0) for p in self.game.b.piece_map().values() if p.color == chess.BLACK)
        diff = w_mat - b_mat
        txt = f"Score: +{diff}" if diff > 0 else (f"Score: {diff}" if diff < 0 else "Score: 0")
        self.lbl_score.config(text=txt)

    def toggle_pause(self):
        if self.game_over: return
        self.paused = not self.paused
        if self.paused:
            self.show_pause_menu()
            self.btn_pause.config(text="RESUME", bg="#388E3C")
        else:
            self.hide_pause_menu()
            self.btn_pause.config(text="PAUSE", bg="#D32F2F")

    def show_pause_menu(self):
        self.pause_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=300, height=200)
        for w in self.pause_menu.winfo_children(): w.destroy()
        tk.Label(self.pause_menu, text="GAME PAUSED", font=("Helvetica", 18, "bold"), bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=20)
        tk.Button(self.pause_menu, text="Resume", command=self.toggle_pause, bg=COLOR_BTN, fg=COLOR_TEXT, width=15).pack(pady=10)
        tk.Button(self.pause_menu, text="Quit to Menu", command=self.show_main_menu, bg="#D32F2F", fg="white", width=15).pack(pady=10)

    def hide_pause_menu(self):
        self.pause_menu.place_forget()

    def on_click(self, event):
        if self.game_over or self.paused or self.ai_thinking or self.animating: return
        if not self.game.turn(): return

        c, r = event.x // SQUARE_SIZE, event.y // SQUARE_SIZE
        if 0 <= c < 8 and 0 <= r < 8:
            sq = chess.square(c, 7-r)
            
            if self.selected_square == sq:
                self.selected_square = None
                self.draw_board()
                return

            if self.selected_square is not None:
                move = chess.Move(self.selected_square, sq)
                if self.game.b.piece_at(self.selected_square).piece_type == chess.PAWN:
                    if (self.game.b.turn == chess.WHITE and chess.square_rank(sq) == 7) or \
                       (self.game.b.turn == chess.BLACK and chess.square_rank(sq) == 0):
                        move = chess.Move(self.selected_square, sq, promotion=chess.QUEEN)

                if move in self.game.b.legal_moves:
                    self.make_move(move)
                    return

            piece = self.game.b.piece_at(sq)
            if piece and piece.color == self.game.b.turn:
                self.selected_square = sq
                self.draw_board()
            else:
                self.selected_square = None
                self.draw_board()

    def start(self):
        self.root.mainloop()
