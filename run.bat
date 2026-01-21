@echo off
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Could not find venv/Scripts/activate.bat
    exit /b 1
)

echo Installing dependencies if missing...
pip install -r requirements.txt > nul 2>&1

echo Starting WhatsApp RAG Chatbot...
python -m uvicorn app.main:app --reload --port 8000
