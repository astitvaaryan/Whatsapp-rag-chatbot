@echo off
echo Starting Ngrok Tunnel...
if not exist "venv" (
    echo Virtual environment not found. Please run run.bat first to set it up.
    pause
    exit /b 1
)

echo Installing pyngrok...
venv\Scripts\python.exe -m pip install pyngrok > nul 2>&1

echo Launching Ngrok...
venv\Scripts\python.exe scripts/start_ngrok.py
