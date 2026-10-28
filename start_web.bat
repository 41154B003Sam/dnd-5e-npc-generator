@echo off
rem ===================================================
rem D&D 5E NPC Generator - Web Server Launcher
rem ===================================================
chcp 65001 >nul

cd /d "%~dp0"

if not exist "server.py" (
    if exist "%USERPROFILE%\OneDrive\Documents\0921test\server.py" (
        cd /d "%USERPROFILE%\OneDrive\Documents\0921test"
    )
)
if not exist "server.py" (
    if exist "%USERPROFILE%\OneDrive\Documents\dnd-5e-npc-generator\server.py" (
        cd /d "%USERPROFILE%\OneDrive\Documents\dnd-5e-npc-generator"
    )
)

if not exist "server.py" (
    echo [提醒] 找不到 server.py，正在直接以瀏覽器開啟網頁介面...
    start "" index.html
    exit /b 0
)

set "PYTHON_EXE="

where python >nul 2>&1
if not errorlevel 1 set "PYTHON_EXE=python"

if not defined PYTHON_EXE (
    where py >nul 2>&1
    if not errorlevel 1 set "PYTHON_EXE=py"
)

if not defined PYTHON_EXE (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    )
)

if not defined PYTHON_EXE (
    echo [提醒] 找不到 Python 環境，正在直接以瀏覽器開啟網頁介面...
    start "" index.html
    exit /b 0
)

echo [啟動中] 正在開啟 D^&D 5E NPC 產生器 本地伺服器...
echo [提示] 瀏覽器將自動開啟 http://127.0.0.1:8765/index.html
echo.
"%PYTHON_EXE%" server.py %*
if errorlevel 1 (
    echo.
    echo [提醒] 伺服器已結束。
    pause
)
