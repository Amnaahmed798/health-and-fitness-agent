@echo off

REM Start message
echo ===============================
echo   Health Coach Application   
echo ===============================
echo.

REM Start Backend
echo [INFO] Starting Backend Server...
start "Backend Server" cmd /k "cd hello_agent && python main.py"
echo [INFO] Backend server started at http://localhost:8000
echo.

REM Start Frontend
if exist frontend (
  echo [INFO] Starting Frontend Server...
  start "Frontend Server" cmd /k "cd frontend && npm run dev"
  echo [INFO] Frontend server starting at http://localhost:3000
) else (
  echo [WARNING] Frontend directory not found. Skipping frontend startup.
)
echo.

echo [INFO] Both servers are starting up...
echo [INFO] Backend API: http://localhost:8000
echo [INFO] Frontend:   http://localhost:3000
echo [INFO] API Docs:   http://localhost:8000/docs
echo.

echo [INFO] Press any key to stop both servers
pause > nul 