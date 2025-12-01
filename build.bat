@echo off
echo ========================================
echo Building ToDoApp Executable
echo ========================================
echo.

echo Step 1: Installing/Upgrading PyInstaller...
pip install --upgrade pyinstaller
echo.

echo Step 2: Building executable with PyInstaller...
pyinstaller ToDoApp.spec --clean
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Your executable is located at:
echo %cd%\dist\ToDoApp.exe
echo.
echo You can now distribute this .exe file to users.
echo They do not need Python installed to run it.
echo.
pause
