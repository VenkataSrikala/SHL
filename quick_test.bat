@echo off
echo ========================================
echo SHL Recommender - Quick Test
echo ========================================
echo.

echo Checking if API is running...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] API is not running!
    echo.
    echo Please start the API first:
    echo   uvicorn api.main:app --reload
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo [OK] API is running!
echo.

echo Testing API...
python test_api.py

echo.
echo ========================================
echo Test complete!
echo ========================================
echo.
echo To use the web UI:
echo   streamlit run frontend/app.py
echo.
pause
