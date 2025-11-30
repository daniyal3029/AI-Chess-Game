# AI Chess Game - Master Edition ♟️

A powerful, interactive Chess application built with Python, featuring multiple AI difficulty levels, a modern GUI, and a self-learning engine.

# AI Chess Game - Master Edition ♟️

A powerful, interactive Chess application built with Python, featuring multiple AI difficulty levels, a modern GUI, and a self-learning engine.

## Team & Roll Numbers
- 23F-3029  
- 23F-3008  
- 23F-3012

## Topic
AI Chess Game with multi-level engines and a self-learning module.

## APIs Used
- python-chess (move generation & validation)  
- Tkinter (GUI)  
- NumPy (data handling)  
- python-docx (optional — for generating Word report)  
- matplotlib (plots for ML metrics, optional)

## Tools
- Python 3.8+  
- Visual Studio Code (recommended)  
- Git / GitHub  
- Windows PowerShell (development / run commands)

## Problem Statement
Design and implement a chess application that:
- Allows human vs AI and AI vs AI play,
- Provides multiple difficulties (Easy / Medium / Hard),
- Learns from played games and updates its memory for future decisions,
- Stores game history and learned memory persistently.

## Deliverables (What to include in the Word document)
Create a Word document (report) that contains:
1. Roll numbers and team member names (listed above).  
2. Project topic and short abstract.  
3. APIs used and brief description for each.  
4. Tools and environment setup instructions.  
5. Problem statement and proposed solution.  
6. Code snippets (key files/functions) with brief explanations:
   - app/Model/game.py — core game loop and rules integration
   - app/Model/engine_med.py — minimax + alpha-beta
   - app/Model/learning.py — memory storage and learning logic
   - app/Controller/main.py — application entrypoint
   - app/View/gui.py — GUI wiring and controls
7. Output screenshots (place images in docs/screenshots and reference them in the doc).  
8. If using ML/LLM or ANN/CNN/GAN, include:
   - Model description and architecture (if applicable),
   - Training/validation metrics (accuracy, loss, other relevant metrics),
   - Plots (loss curves, accuracy curves, confusion matrix, etc.),
   - Saved model file paths and how to reproduce training (if training was performed).

## Where to place code snippets & screenshots
- Put screenshots in: `docs/screenshots/` (create if missing).  
- Example memory and history files: `data/memory.json`, `data/history.json`.

## Example Metrics Table (for ML/LLM projects)
| Metric | Train | Validation |
|--------|-------|------------|
| Accuracy | 0.92 | 0.89 |
| Loss     | 0.18 | 0.22 |

(Replace with real values and include plots in `docs/screenshots/` referenced from the Word doc.)

## How to generate the Word document (optional, automated)
You can use python-docx to generate a basic report:
1. Install: `pip install python-docx`
2. Create a small script to insert headings, text, code snippets (as preformatted text) and images from `docs/screenshots/`.

Example script hint (not full script):
- Place code snippets by reading files and adding them as runs with a monospace font.
- Add images with doc.add_picture('docs/screenshots/example.png').

## How to run the project
From project root (Windows PowerShell):
```powershell
# activate venv
.\.venv\Scripts\activate
# run controller as module
python -m app.Controller.main
```
If module import errors occur, run from project root directory (`E:\Chess-game`) and ensure `app` package is importable.

## Notes
- If the project uses any pre-trained models, include model files and metrics in the report.  
- Replace placeholder metric values and screenshots with actual outputs before final submission.

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
