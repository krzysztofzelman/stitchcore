#!/bin/bash
# StitchCore — setup script

set -e

echo "=== StitchCore Setup ==="

# Backend
echo "[1/3] Backend..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env 2>/dev/null || true
cd ..

# Frontend-shop
echo "[2/3] Frontend Shop..."
cd frontend-shop
npm install
cd ..

# Frontend-admin
echo "[3/3] Frontend Admin..."
cd frontend-admin
npm install
cd ..

echo ""
echo "=== Setup complete ==="
echo ""
echo "To run:"
echo "  Terminal 1: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "  Terminal 2: cd frontend-shop && npm run dev"
echo "  Terminal 3: cd frontend-admin && npm run dev"
