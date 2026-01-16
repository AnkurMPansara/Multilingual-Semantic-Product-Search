@echo off

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found. Creating...
    python -m venv .venv

    echo Installing requirements...
    call .venv\Scripts\pip install -r requirements.txt
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Load variables from .env file
if exist ".env" (
    echo Loading environment variables from .env...

    for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
        set %%a=%%b
    )
) else (
    echo No .env file found, skipping...
)

REM Run the application
echo Running main.py...
python main.py

pause
