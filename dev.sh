#!/bin/bash

echo "Starting Health Coach Application..."
echo

echo "Starting Backend Server..."
(cd hello_agent && python main.py) &
BACKEND_PID=$!

echo "Backend server started at http://localhost:8000"
echo

echo "Starting Frontend Server..."
if [ -d "frontend" ]; then
  (cd frontend && npm run dev) &
  FRONTEND_PID=$!
  echo "Frontend server starting at http://localhost:3000"
else
  echo "[WARNING] Frontend directory not found. Skipping frontend startup."
  FRONTEND_PID=""
fi
echo

echo "Both servers are starting up..."
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo

echo "Press Ctrl+C to stop both servers"
echo

# Wait for both processes
if [ -n "$FRONTEND_PID" ]; then
  wait $BACKEND_PID $FRONTEND_PID
else
  wait $BACKEND_PID
fi

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT 