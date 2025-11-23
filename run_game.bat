@echo off
REM Run the Chess Game using the virtual environment
echo Starting Chess AI...
".\.venv\Scripts\python.exe" -m app.Controller.main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: Game crashed or failed to start.
    pause
)
