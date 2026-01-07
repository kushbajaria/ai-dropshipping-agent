#!/bin/bash

# Full Stack Setup Script
# Installs and starts both backend and frontend

set -e

echo "🚀 AI Dropshipping Agent - Full Stack Setup"
echo "==========================================="

# Backend Setup
echo ""
echo "📦 Setting up backend..."
cd backend

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "✅ Backend dependencies installed"

# Frontend Setup
echo ""
echo "📦 Setting up frontend..."
cd ../frontend

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required"
    exit 1
fi

if [ ! -d "node_modules" ]; then
    npm install
fi

echo "✅ Frontend dependencies installed"

echo ""
echo "==========================================="
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "1. Backend:"
echo "   cd backend"
echo "   source venv/bin/activate  # on macOS/Linux"
echo "   python -m uvicorn app.main:app --reload"
echo ""
echo "2. Frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "Then visit: http://localhost:3000"
echo "==========================================="
