@echo off
cd /d "%~dp0"
start "" pythonw server.py
if %errorlevel% neq 0 (
    start "" "%~dp0index.html"
)
