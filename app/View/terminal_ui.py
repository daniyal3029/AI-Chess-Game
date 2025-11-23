# app/view/terminal_ui.py
# Simple terminal view

import sys

def show_board(game):
    # game: Game instance
    print()
    print(game.unicode())
    print()

def ask_move(prompt="Your move (uci or SAN, 'q' to quit): "):
    try:
        s = input(prompt).strip()
    except EOFError:
        s = 'q'
    return s

def show_msg(msg):
    print(msg)

def choose_level():
    print("Choose difficulty level:")
    print("1 - Easy")
    print("2 - Medium")
    print("3 - Hard")
    while True:
        try:
            v = input("level (1/2/3): ").strip()
        except EOFError:
            v = "1"
        if v in ("1","2","3"):
            return int(v)
        print("enter 1, 2, or 3")
