#!/bin/bash

# Bisounours - Script pour tuer et relancer les serveurs

echo "🔴 Arrêt des serveurs..."
pkill -f "npm run dev" || true
pkill -f "vite" || true
pkill -f "python.*main.py" || true
sleep 1

echo "🟢 Lancement du backend..."
cd /home/willysmile/Documents/Gestion_des_plantes/backend
source /home/willysmile/Documents/Gestion_des_plantes/backend/venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

sleep 3

echo "🟢 Lancement du frontend..."
cd /home/willysmile/Documents/Gestion_des_plantes/frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ Serveurs lancés!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Logs:"
echo "   Backend:  tail -f /tmp/backend.log"
echo "   Frontend: tail -f /tmp/frontend.log"
