@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Check Python version
for /F "tokens=2 delims= " %%i in ('python --version') do set pyver=%%i
echo Found Python version !pyver!

:: Extract major and minor version
for /f "tokens=1,2 delims=." %%a in ("!pyver!") do (
  set pymajor=%%a
  set pyminor=%%b
)

:: Check if major is 3 and minor is 10, 11, or 12
if "!pymajor!"=="3" if "!pyminor!"=="10" goto valid_version
if "!pymajor!"=="3" if "!pyminor!"=="11" goto valid_version
if "!pymajor!"=="3" if "!pyminor!"=="12" goto valid_version

echo Your Python version does not meet the requirements.
echo This script requires Python 3.10, 3.11, or 3.12.
exit /b

:valid_version
echo Proceeding with Python version !pyver!

python -m venv venv
call .\venv\scripts\activate
call python -m pip install --upgrade pip
call pip install -r requirements.txt

echo Installation successful. Run "run.bat" to run the app.
ENDLOCAL
pause
