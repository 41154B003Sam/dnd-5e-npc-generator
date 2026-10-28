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
    echo [錯誤] 找不到 Python 執行檔！
    echo 請確認電腦已安裝 Python 3.10+
    pause
    exit /b 1
)

echo [啟動中] 正在開啟 D&D 5E 視窗程式...
%PY_CMD% gui.py
if %errorlevel% neq 0 (
    echo.
    echo [執行出錯] 請檢查上方錯誤訊息。
    pause
)
