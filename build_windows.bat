@echo off
setlocal
py -m pip install -r requirements.txt
py -m PyInstaller --noconfirm --clean --onedir --windowed --name "MIDI Forge Portable" --collect-all customtkinter main.py
echo.
echo Build complete: dist\MIDI Forge Portable\MIDI Forge Portable.exe
endlocal
