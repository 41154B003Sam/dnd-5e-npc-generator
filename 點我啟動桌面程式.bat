@echo off
rem ===================================================
rem D&D 5E NPC Generator - GUI Launcher
rem ===================================================
chcp 65001 >nul

cd /d "%~dp0"

if not exist "gui.py" (
    if exist "%USERPROFILE%\OneDrive\Documents\0921test\gui.py" (
        cd /d "%USERPROFILE%\OneDrive\Documents\0921test"
    )
)
if not exist "gui.py" (
    if exist "%USERPROFILE%\OneDrive\Documents\dnd-5e-npc-generator\gui.py" (
        cd /d "%USERPROFILE%\OneDrive\Documents\dnd-5e-npc-generator"
    )
)

if not exist "gui.py" (
    echo [錯誤] 找不到 gui.py 程式檔案！
    echo 請確認本批次檔與專案檔案放置於同一資料夾。
    echo 目前目錄：%CD%
    echo.
    pause
    exit /b 1
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
    echo [錯誤] 找不到 Python 執行環境！
    echo 請至 https://www.python.org 安裝 Python 3.10 以上版本，
    echo 並在安裝時勾選「Add python.exe to PATH」。
    echo.
    pause
    exit /b 1
)

echo [啟動中] 正在開啟 D^&D 5E NPC 視窗程式...
"%PYTHON_EXE%" gui.py %*
if errorlevel 1 (
    echo.
    echo [執行錯誤] 程式異常結束，請檢查上方錯誤訊息。
    pause
)
