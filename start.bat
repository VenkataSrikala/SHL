@echo off
echo ========================================
echo SHL Assessment Recommender
echo ========================================
echo.

REM Check if setup is complete
if not exist "vector_db\index.faiss" (
    echo Setup not complete. Running setup...
    echo.
    python setup.py --scraper mock
    echo.
)

echo Starting API server...
echo.
start cmd /k "uvicorn api.main:app --reload"

timeout /t 3 /nobreak > nul

echo Starting web interface...
echo.
start cmd /k "streamlit run frontend/app.py"

echo.
echo ========================================
echo System started!
echo ========================================
echo API: http://localhost:8000
echo UI:  http://localhost:8501
echo.
echo Press any key to exit...
pause > nul
