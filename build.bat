@echo off
setlocal

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

if not exist "dist\ExarotonRemote.exe" (
    echo.
    echo Build failed - ExarotonRemote.exe not found.
    pause
    exit /b 1
)

echo.
echo Build complete!
echo.

:: ------------------------------------------------------------------ Install?
set INSTALL_DIR=%LOCALAPPDATA%\ExarotonRemote
set /p DO_INSTALL="Copy to %INSTALL_DIR%? [Y/n]: "
if /i "%DO_INSTALL%"=="n" goto :shortcut_prompt

echo Copying to %INSTALL_DIR% ...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
copy /y "dist\ExarotonRemote.exe" "%INSTALL_DIR%\ExarotonRemote.exe" >nul
echo Done.

:: ------------------------------------------------------------------ Shortcut?
:shortcut_prompt
echo.
set /p DO_SHORTCUT="Create a desktop shortcut? [Y/n]: "
if /i "%DO_SHORTCUT%"=="n" goto :done

:: Determine shortcut target — prefer the installed copy if it exists
set SHORTCUT_TARGET=%INSTALL_DIR%\ExarotonRemote.exe
if not exist "%SHORTCUT_TARGET%" set SHORTCUT_TARGET=%~dp0dist\ExarotonRemote.exe

echo Creating desktop shortcut ...
powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell;" ^
  "$sc = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\ExarotonRemote.lnk');" ^
  "$sc.TargetPath = '%SHORTCUT_TARGET%';" ^
  "$sc.WorkingDirectory = [System.IO.Path]::GetDirectoryName('%SHORTCUT_TARGET%');" ^
  "$sc.Description = 'Exaroton Remote';" ^
  "$sc.Save()"
echo Done.

:done
echo.
echo All finished! You can also right-click the exe and choose "Pin to Start".
pause
endlocal
