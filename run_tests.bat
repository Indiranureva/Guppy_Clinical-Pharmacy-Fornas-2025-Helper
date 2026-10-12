@echo off
setlocal enabledelayedexpansion
title Guppy - Test Suite Runner

cd /d "%~dp0"

set "PYTHON_EXE="
where py >nul 2>nul && set "PYTHON_EXE=py"
if "%PYTHON_EXE%"=="" where python >nul 2>nul && set "PYTHON_EXE=python"
if "%PYTHON_EXE%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"

if "%PYTHON_EXE%"=="" (
    echo Python not found.
    pause
    exit /b 1
)

%PYTHON_EXE% -m pytest tests -v
pause
