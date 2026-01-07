#!/bin/bash

# Start both backend and frontend
# Run this script to start the entire application

set -e

echo "🚀 Starting AI Dropshipping Agent"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend is running
echo ""
echo "📍 Starting backend..."
cd backend
source venv/bin/activate 2>/dev/null || true

python -m uvicorn app.main:app --reload &
BACKEND_PID=$!

echo "✅ Backend started (PID: $BACKEND_PID)"
sleep 2

# Check if backend is responding
if ! curl -s http://localhost:8000/products/health -H "X-API-Key: test-key-123" > /dev/null 2>&1; then
    echo -e "${RED}❌ Backend not responding. Check if it started correctly.${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Backend is responding"

# Start frontend
echo ""
echo "📍 Starting frontend..."
cd ../frontend

npm run dev &
FRONTEND_PID=$!

echo "✅ Frontend started (PID: $FRONTEND_PID)"
sleep 3

echo ""
echo "=================================="
echo -e "${GREEN}✅ Application started!${NC}"
echo "=================================="
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Keep script running
wait $BACKEND_PID $FRONTEND_PID
