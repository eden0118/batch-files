@echo off
REM Build Windows application for Batch Renamer

echo ==========================================
echo Building Batch Renamer for Windows
echo ==========================================

REM Install dependencies
echo Installing dependencies...
pip3 install -q flet pyinstaller

REM Clean up previous builds
echo Cleaning up previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "Batch Renamer.exe" del "Batch Renamer.exe"

REM Build the application
echo Building application...
python3 -m PyInstaller ^
    --name "Batch Renamer" ^
    --onefile ^
    --windowed ^
    --collect-all flet ^
    main.py

echo ==========================================
echo Build complete!
echo Application: dist/Batch Renamer.exe
echo ==========================================
pause
