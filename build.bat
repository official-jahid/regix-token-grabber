@echo off
cls
color 0A
title REGIX QUEST Token Grabber - Build Tool

echo ================================================
echo    REGIX QUEST Token Grabber - Professional Edition
echo ================================================
echo.

:MENU
echo [1] Install Dependencies
echo [2] Run REGIX QUEST (Normal Mode)
echo [3] Run REGIX QUEST (Dry Run Mode)
echo [4] Run REGIX QUEST (Silent Mode)
echo [5] Build Executable (PyInstaller)
echo [6] Build Executable (Stealth Mode)
echo [7] Test Configuration
echo [8] Clean Build Files
echo [9] Exit
echo.
set /p choice="Select an option (1-8): "

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto RUN_NORMAL
if "%choice%"=="3" goto RUN_DRYRUN
if "%choice%"=="4" goto RUN_SILENT
if "%choice%"=="5" goto BUILD_EXE
if "%choice%"=="6" goto BUILD_STEALTH
if "%choice%"=="7" goto TEST_CONFIG
if "%choice%"=="8" goto CLEAN
if "%choice%"=="9" goto EXIT

echo Invalid option! Please try again.
echo.
pause
cls
goto MENU

:INSTALL
echo.
echo Installing dependencies...
echo.
python setup.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to install dependencies!
    pause
    goto MENU
)
echo.
echo Dependencies installed successfully!
echo.
pause
cls
goto MENU

:RUN_NORMAL
echo.
echo Running REGIX QUEST in normal mode...
echo.
python regix_quest.py
echo.
echo REGIX QUEST execution completed!
echo.
pause
cls
goto MENU

:RUN_DRYRUN
echo.
echo Running REGIX QUEST in DRY RUN mode (no webhooks)...
echo.
python regix_quest.py --dry-run
echo.
echo Dry run completed!
echo.
pause
cls
goto MENU

:RUN_SILENT
echo.
echo Running REGIX QUEST in SILENT mode...
echo.
python regix_quest.py --silent
echo.
echo Silent execution completed!
echo.
pause
cls
goto MENU

:BUILD_EXE
echo.
echo Building executable with PyInstaller...
echo.
echo Checking if PyInstaller is installed...
python -c "import PyInstaller" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
)
echo.
echo Building RegixQuest.exe...
python builder.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo Build successful!
    echo Executable location: dist\RegixQuest.exe
    echo ================================================
) else (
    echo.
    echo ERROR: Build failed!
)
echo.
pause
cls
goto MENU

:BUILD_STEALTH
echo.
echo Building executable (Stealth Mode)...
echo.
echo Checking if PyInstaller is installed...
python -c "import PyInstaller" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
)
echo.
echo Building RegixQuest_Stealth.exe...
python builder.py --stealth

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo Build successful!
    echo Executable location: dist\RegixQuest_Stealth.exe
    echo ================================================
) else (
    echo.
    echo ERROR: Build failed!
)
echo.
pause
cls
goto MENU

:TEST_CONFIG
echo.
echo Testing configuration...
echo.
python regix_quest.py --dry-run --config config.json
echo.
echo Configuration test completed!
echo.
pause
cls
goto MENU

:CLEAN
echo.
echo Cleaning build files...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist __pycache__ rd /s /q __pycache__
if exist *.spec del /q *.spec
echo.
echo Build files cleaned!
echo.
pause
cls
goto MENU

:EXIT
echo.
echo Thank you for using REGIX QUEST!
echo.
timeout /t 2 >nul
exit
