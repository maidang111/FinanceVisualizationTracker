#!/bin/bash

echo "Starting backend..."
cd lumon-backend
source ../.venv/bin/activate
uvicorn main:app --reload &
BACKEND_PID=$!

echo "Starting frontend..."
cd ../lumon-frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both."

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
