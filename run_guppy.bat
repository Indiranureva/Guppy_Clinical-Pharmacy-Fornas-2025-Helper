@echo off
setlocal
title Guppy - Clinical Pharmacy and Fornas 2025 Helper

cd /d "%~dp0"

echo ======================================================================
echo   GUPPY - Clinical Pharmacy and Fornas 2025 Helper
echo ======================================================================
echo.

if not exist guppy\frontend\app.py (
    echo [ERROR] File guppy\frontend\app.py tidak ditemukan!
    echo.
    echo Pastikan:
    echo 1. File ZIP hasil unduhan Google Drive sudah diekstrak sepenuhnya.
    echo 2. File run_guppy.bat dijalankan dari dalam folder hasil ekstrak.
    echo.
    pause
    exit /b 1
)

echo [*] Mendeteksi Python di komputer...

set PY_EXE=
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 set PY_EXE=py -3

if "%PY_EXE%"=="" (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 set PY_EXE=python
)

if "%PY_EXE%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set PY_EXE="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
)
if "%PY_EXE%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set PY_EXE="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)
if "%PY_EXE%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set PY_EXE="%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
)
if "%PY_EXE%"=="" (
    if exist "C:\Python311\python.exe" set PY_EXE="C:\Python311\python.exe"
)
if "%PY_EXE%"=="" (
    if exist "C:\Python312\python.exe" set PY_EXE="C:\Python312\python.exe"
)
if "%PY_EXE%"=="" (
    if exist "C:\Python310\python.exe" set PY_EXE="C:\Python310\python.exe"
)

if "%PY_EXE%"=="" (
    echo ======================================================================
    echo [PERINGATAN] Python belum terpasang di komputer ini!
    echo ======================================================================
    echo Silakan unduh dan install Python:
    echo 1. Website: https://www.python.org/downloads/
    echo 2. PENTING: Beri centang pada [X] "Add python.exe to PATH"
    echo 3. Setelah selesai, buka kembali file run_guppy.bat ini.
    echo ======================================================================
    echo.
    pause
    exit /b 1
)

echo [*] Menggunakan Python: %PY_EXE%
echo [*] Memeriksa paket dependensi (Streamlit, python-docx, pytest)...

%PY_EXE% -c "import streamlit, docx" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [*] Mengunduh dan memasang paket pendukung otomatis...
    %PY_EXE% -m pip install streamlit pytest python-docx
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Gagal memasang dependensi. Pastikan PC terhubung ke internet.
        pause
        exit /b 1
    )
)

echo.
echo ======================================================================
echo [*] Membuka Guppy di Web Browser...
echo ======================================================================
echo.

%PY_EXE% -m streamlit run guppy\frontend\app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Terjadi kesalahan saat menjalankan aplikasi.
    pause
)
