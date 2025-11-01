#!/bin/bash

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🧸 Bisounours - Redémarrage des serveurs${NC}"

# Arrêter les serveurs existants
echo -e "${YELLOW}🛑 Arrêt des serveurs...${NC}"
pkill -f "uvicorn app.main" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
sleep 2

# Démarrer le backend
echo -e "${YELLOW}🚀 Démarrage du backend...${NC}"
cd /home/willysmile/Documents/Gestion_des_plantes/backend
./venv/bin/python -m uvicorn app.main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend démarré (PID: $BACKEND_PID)${NC}"

# Attendre que le backend soit prêt
sleep 3

# Démarrer le frontend
echo -e "${YELLOW}🚀 Démarrage du frontend...${NC}"
cd /home/willysmile/Documents/Gestion_des_plantes/frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend démarré (PID: $FRONTEND_PID)${NC}"

echo ""
echo -e "${GREEN}🎉 Tous les serveurs sont en cours d'exécution!${NC}"
echo ""
echo -e "Backend:  ${GREEN}http://localhost:8000${NC}"
echo -e "Frontend: ${GREEN}http://localhost:5173${NC}"
echo ""
echo -e "Pour voir les logs:"
echo -e "  Backend:  ${YELLOW}tail -f /tmp/backend.log${NC}"
echo -e "  Frontend: ${YELLOW}tail -f /tmp/frontend.log${NC}"
