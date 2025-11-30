@echo off
REM Script to run Selenium E2E tests on Windows

echo ============================================================
echo   CMMS Selenium E2E Test Runner
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

REM Check if pytest is installed
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo ERROR: pytest is not installed
    echo Run: pip install pytest
    exit /b 1
)

REM Check if selenium is installed
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Selenium is not installed
    echo Run: pip install -r requirements-test.txt
    exit /b 1
)

echo All dependencies are installed
echo.

REM Check if services are running
echo Checking if services are running...
curl -s http://localhost:8000/api/v1/ >nul 2>&1
if errorlevel 1 (
    echo WARNING: Backend is not running at http://localhost:8000
    echo Start it with: python manage.py runserver
    echo.
)

curl -s http://localhost:5173/ >nul 2>&1
if errorlevel 1 (
    echo WARNING: Frontend is not running at http://localhost:5173
    echo Start it with: npm run dev
    echo.
)

echo.
echo Running Selenium tests...
echo.

REM Run tests
if "%1"=="" (
    pytest tests_selenium/ -v --tb=short
) else (
    pytest %1 -v --tb=short
)

if errorlevel 1 (
    echo.
    echo ============================================================
    echo   Some tests failed
    echo ============================================================
    exit /b 1
) else (
    echo.
    echo ============================================================
    echo   All tests passed!
    echo ============================================================
    exit /b 0
)
