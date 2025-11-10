#!/bin/bash

set -e

PROJECT_ROOT="/home/willysmile/Documents/Gestion_des_plantes"
BACKEND_VENV="$PROJECT_ROOT/backend/venv/bin/python"
BACKEND_PORT=8000
FRONTEND_PORT=5173

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${RESET}"
echo -e "${BLUE}║     🌱 Gestion des Plantes - Démarrage Serveurs       ║${RESET}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${RESET}"
echo ""

# 1. Killer tous les processus existants
echo -e "${YELLOW}[1/4]${RESET} Arrêt des serveurs existants..."

# Kill Python processes on port 8000
if lsof -Pi :$BACKEND_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "  ⚠️  Port $BACKEND_PORT en utilisation, nettoyage..."
  lsof -ti:$BACKEND_PORT | xargs -r kill -9 2>/dev/null || true
  sleep 1
fi

# Kill npm processes
if pgrep -f "npm.*dev" >/dev/null 2>&1; then
  echo "  ⚠️  Processus npm en cours, nettoyage..."
  pkill -9 -f "npm.*dev" 2>/dev/null || true
fi

# Kill Python processes
if pgrep -f "app.main" >/dev/null 2>&1; then
  echo "  ⚠️  Processus Python en cours, nettoyage..."
  pkill -9 -f "app.main" 2>/dev/null || true
fi

sleep 2

# 2. Démarrer le Backend
echo -e "${YELLOW}[2/4]${RESET} Démarrage du Backend..."
cd "$PROJECT_ROOT/backend"

# Clear old logs
> /tmp/backend.log

# Start backend
$BACKEND_VENV -m app.main > /tmp/backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "  ⏳ Démarrage du serveur (PID: $BACKEND_PID)..."
sleep 5

# Check if backend is running
if kill -0 $BACKEND_PID 2>/dev/null; then
  # Try to reach the backend
  if curl -s http://localhost:$BACKEND_PORT/api/plants >/dev/null 2>&1; then
    echo -e "  ${GREEN}✅ Backend démarré avec succès${RESET}"
  else
    echo -e "  ${YELLOW}⚠️  Processus actif mais pas de réponse yet...${RESET}"
    sleep 2
  fi
else
  echo -e "  ${RED}❌ Backend n'a pas démarré${RESET}"
  echo -e "  ${RED}Erreur:${RESET}"
  tail -15 /tmp/backend.log
  exit 1
fi

# 3. Démarrer le Frontend
echo -e "${YELLOW}[3/4]${RESET} Démarrage du Frontend..."
cd "$PROJECT_ROOT/frontend"

# Clear old logs
> /tmp/frontend.log

# Kill any process on port 5173
if lsof -Pi :$FRONTEND_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "  ⚠️  Port $FRONTEND_PORT en utilisation, nettoyage..."
  lsof -ti:$FRONTEND_PORT | xargs -r kill -9 2>/dev/null || true
  sleep 1
fi

# Start frontend with explicit port
npm run dev -- --port $FRONTEND_PORT --host 127.0.0.1 > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!

echo "  ⏳ Démarrage du serveur (PID: $FRONTEND_PID)..."
sleep 8

# Check if frontend is running
if kill -0 $FRONTEND_PID 2>/dev/null; then
  echo -e "  ${GREEN}✅ Frontend démarré avec succès${RESET}"
else
  echo -e "  ${RED}❌ Frontend n'a pas démarré${RESET}"
  echo -e "  ${RED}Erreur:${RESET}"
  tail -15 /tmp/frontend.log
  exit 1
fi

# 4. Afficher le statut
echo -e "${YELLOW}[4/4]${RESET} Vérification des serveurs..."
sleep 2

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}║              🎉 Serveurs opérationnels!              ║${RESET}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "${BLUE}📊 Backend${RESET}"
echo -e "  URL:    ${GREEN}http://localhost:$BACKEND_PORT${RESET}"
echo -e "  PID:    $BACKEND_PID"
echo -e "  Status: ${GREEN}✓ Running${RESET}"
echo ""
echo -e "${BLUE}🎨 Frontend${RESET}"
echo -e "  URL:    ${GREEN}http://localhost:$FRONTEND_PORT${RESET}"
echo -e "  PID:    $FRONTEND_PID"
echo -e "  Status: ${GREEN}✓ Running${RESET}"
echo ""
echo -e "${BLUE}📝 Logs${RESET}"
echo -e "  Backend:  ${YELLOW}tail -f /tmp/backend.log${RESET}"
echo -e "  Frontend: ${YELLOW}tail -f /tmp/frontend.log${RESET}"
echo ""
echo -e "${BLUE}🛑 Arrêt${RESET}"
echo -e "  Appuyer sur ${RED}Ctrl+C${RESET} pour arrêter les serveurs"
echo ""

wait
