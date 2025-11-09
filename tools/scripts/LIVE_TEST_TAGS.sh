#!/bin/bash

# Couleurs
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${YELLOW}🚀 LIVE TESTING - Session Tags System${NC}\n"

# Check if bisounours runs the servers
echo -e "${YELLOW}Starting services with bisounours.sh...${NC}"
bash /home/willysmile/Documents/Gestion_des_plantes/bisounours.sh

sleep 5

echo ""
echo -e "${GREEN}✅ Services started!${NC}"
echo -e "${YELLOW}Available URLs:${NC}"
echo -e "  Backend API:  ${GREEN}http://localhost:8000${NC}"
echo -e "  Frontend:     ${GREEN}http://localhost:5173${NC}"
echo -e "  API Docs:     ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}To monitor logs:${NC}"
echo -e "  Backend:  ${GREEN}tail -f /tmp/backend.log${NC}"
echo -e "  Frontend: ${GREEN}tail -f /tmp/frontend.log${NC}"
echo ""
echo -e "${YELLOW}Tests to run manually:${NC}"
echo -e "  1. Add new plant with tags in form"
echo -e "  2. View plant in modal - see tags displayed"
echo -e "  3. Edit plant - modify tags"
echo -e "  4. Go to Settings > Tags - manage custom tags"
echo -e "  5. Delete plant - verify archive/restore"
echo ""
echo -e "${YELLOW}⏳ Services running... Press Ctrl+C to stop${NC}\n"

wait
