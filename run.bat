@echo off
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies.
    pause
    exit /b %errorlevel%
)

echo Dependencies installed successfully.
echo Running main.py...
python main.py

if %errorlevel% neq 0 (
    echo Error: Failed to run main.py.
    pause
    exit /b %errorlevel%
)

echo Application has finished running.
pause
