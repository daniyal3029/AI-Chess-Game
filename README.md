# AI Chess Game - Master Edition ♟

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

## Getting Started
To get started with the project, follow these steps:
1. Clone the repository: `git clone https://github.com/daniyal3029/AI-Chess-Game.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the application: `python app/Controller/main.py`

## Contributing
If you'd like to contribute to the project, please fork the repository, make your changes, and submit a pull request. We appreciate any contributions, whether it's a bug fix, a new feature, or documentation improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.