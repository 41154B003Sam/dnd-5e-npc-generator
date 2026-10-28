@echo off
cd /d "%~dp0"
start "" pythonw gui.py
if %errorlevel% neq 0 (
    python gui.py
)
