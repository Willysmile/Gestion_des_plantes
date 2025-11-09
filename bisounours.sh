#!/bin/bash

PROJECT_ROOT="/home/willysmile/Documents/Gestion_des_plantes"

echo "Arrêt des serveurs existants..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "npm.*dev" 2>/dev/null
sleep 2

echo "Démarrage du Backend..."
cd "$PROJECT_ROOT/backend"
python3 -m app.main > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
sleep 3

echo "Démarrage du Frontend..."
cd "$PROJECT_ROOT/frontend"
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 2

echo ""
echo "Backend:  http://localhost:8000  (PID: $BACKEND_PID)"
echo "Frontend: http://localhost:5173  (PID: $FRONTEND_PID)"
echo ""
echo "Logs:"
echo "  Backend:  tail -f /tmp/backend.log"
echo "  Frontend: tail -f /tmp/frontend.log"
echo ""

wait
