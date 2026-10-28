@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "PY_CMD="

where python >nul 2>&1
if %errorlevel% equ 0 set "PY_CMD=python"

if "%PY_CMD%"=="" (
    where py >nul 2>&1
    if %errorlevel% equ 0 set "PY_CMD=py -3"
)

if "%PY_CMD%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    )
)

if "%PY_CMD%"=="" (
    echo [提醒] 找不到 Python 環境，正在直接以瀏覽器開啟網頁介面...
    start "" "%~dp0index.html"
    exit /b 0
)

echo [啟動中] 正在啟動 D&D 5E NPC 產生器 本地伺服器...
echo [提示] 瀏覽器將自動開啟 http://127.0.0.1:8765/index.html
echo.
%PY_CMD% server.py
if %errorlevel% neq 0 (
    echo.
    echo [伺服器異常或已關閉] 正在嘗試直接開啟 index.html...
    start "" "%~dp0index.html"
    pause
)
