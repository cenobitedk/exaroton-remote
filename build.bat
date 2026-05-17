@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building ExarotonRemote.exe ...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "ExarotonRemote" ^
    --collect-all customtkinter ^
    --collect-all pystray ^
    --hidden-import PIL ^
    --hidden-import PIL._imagingtk ^
    app.py

echo.
echo Done! Find ExarotonRemote.exe in the dist\ folder.
echo.
echo To install:
echo   1. Copy dist\ExarotonRemote.exe somewhere permanent (e.g. C:\Users\YourName\AppData\Local\ExarotonRemote\)
echo   2. Right-click the .exe and choose "Pin to Start" or "Create shortcut"
echo   3. Launch it once - use the tray icon menu to enable "Start with Windows"
pause
