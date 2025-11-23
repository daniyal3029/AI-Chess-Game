# AI Chess Game - Master Edition ♟️

A powerful, interactive Chess application built with Python, featuring multiple AI difficulty levels, a modern GUI, and a self-learning engine.

![Chess GUI](https://img.shields.io/badge/GUI-Tkinter-blue) ![AI](https://img.shields.io/badge/AI-Minimax%20%2B%20Learning-green) ![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)

## ✨ Features

*   **🧠 Advanced AI Engine**:
    *   **Easy**: Random moves with basic capture logic.
    *   **Medium**: Minimax algorithm with Alpha-Beta pruning.
    *   **Hard**: Neural Network evaluation (falls back to robust Minimax if model missing).
*   **🎓 Self-Learning System**: The AI learns from every game played! It remembers winning moves and uses them in future matches.
*   **🎨 Modern UI**:
    *   Clean Gray-Black-White theme.
    *   **Piece Animation**: Smooth sliding movements.
    *   **Move Highlighting**: Legal moves, captures, and checks are clearly marked.
*   **📜 Game History**: Tracks all your matches with results, dates, and difficulty levels.
*   **⏸️ Game Controls**: Pause/Resume functionality and a live Scoreboard.

## 🚀 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/daniyal3029/AI-Chess-Game.git
    cd AI-Chess-Game
    ```

2.  **Set up a Virtual Environment** (Recommended):
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🎮 How to Play

**Windows Users**:
Simply double-click the `run_game.bat` file!

**Manual Start**:
```bash
python -m app.Controller.main
```

### Controls
*   **Left Click**: Select piece / Move piece.
*   **Pause Button**: Pause the game.
*   **Main Menu**: Select difficulty or view history.

## 📂 Project Structure

*   `app/Model`: Game logic, AI engines, and Learning system.
*   `app/View`: GUI implementation using Tkinter.
*   `app/Controller`: Main entry point and coordination.
*   `data/`: Stores learned memory (`memory.json`) and game history (`history.json`).

## 🛠️ Technologies

*   **Python 3**: Core language.
*   **Tkinter**: Graphical User Interface.
*   **python-chess**: Move generation and validation.
*   **NumPy**: Data manipulation for AI.

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a Pull Request.

---
*Developed by Daniyal Haider*
