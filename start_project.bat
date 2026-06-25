@echo off
echo ===========================================
echo   Starting VatteluttuX OCR System
echo ===========================================

echo.
echo [1/2] Starting Backend Server...
start "VatteluttuX Backend" cmd /k "cd backend && pip install -r requirements.txt && python run.py"

echo.
echo [2/2] Starting Frontend Server...
start "VatteluttuX Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ===========================================
echo   System is starting up!
echo   Frontend will be at: http://localhost:5173
echo   Backend will be at: http://localhost:8000
echo ===========================================
pause
