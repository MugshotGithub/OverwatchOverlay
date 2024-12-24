@echo off
REM Check if we are already in a virtual environment
if not defined VIRTUAL_ENV (
    echo Not in a virtual environment. Activating the virtual environment...
    REM Change this to the actual path to your virtual environment's Scripts directory
    call .venv\Scripts\activate
)
python main.py