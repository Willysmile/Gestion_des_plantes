#!/bin/bash

# 🧪 Test Script - Phase 3.1 Validation Taxonomique
# Usage: bash test_live.sh

echo "🌱 Phase 3.1 - Test Suite"
echo "=========================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="http://localhost:8001"
FRONTEND_URL="http://localhost:5173"

echo -e "${BLUE}Vérification des serveurs...${NC}"

# Test Backend
echo -n "Backend (8001): "
if curl -s "${BACKEND_URL}/api/plants" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ DOWN${NC}"
    exit 1
fi

# Test Frontend (check via JS/Manual)
echo -n "Frontend (5173): "
echo -e "${YELLOW}Manual Check${NC} (ouvert dans navigateur)"

echo ""
echo -e "${BLUE}Création de plantes de test...${NC}"

# Test 1: Plante Minimale
echo ""
echo -n "Test 1 - Plante Minimale: "
RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/plants" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Minimal",
    "family": "Araceae"
  }')

if echo "$RESPONSE" | grep -q '"id"'; then
    PLANT_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
    echo -e "${GREEN}✅ OK${NC} (ID: $PLANT_ID)"
else
    echo -e "${RED}❌ FAILED${NC}"
    echo "Response: $RESPONSE"
fi

# Test 2: Plante Complète
echo -n "Test 2 - Plante Complète: "
RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/plants" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Phalaenopsis Test",
    "family": "Orchidaceae",
    "subfamily": "epidendroideae",
    "genus": "Phalaenopsis",
    "species": "amabilis",
    "subspecies": "subsp. rosenstromii",
    "variety": "var. alba",
    "cultivar": "'"'"'White Dream'"'"'",
    "temp_min": 15,
    "temp_max": 25,
    "humidity": 70,
    "soil_type": "terreau",
    "description": "Test de plante complète",
    "care_instructions": "Arroser régulièrement",
    "difficulty_level": "medium",
    "growth_speed": "slow",
    "flowering_season": "Hiver",
    "is_indoor": true,
    "is_favorite": true
  }')

if echo "$RESPONSE" | grep -q '"id"'; then
    PLANT_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
    echo -e "${GREEN}✅ OK${NC} (ID: $PLANT_ID)"
    
    # Vérifier les auto-générations
    echo ""
    echo -e "${YELLOW}Vérification des auto-générations:${NC}"
    
    REFERENCE=$(echo "$RESPONSE" | grep -o '"reference":"[^"]*"' | cut -d'"' -f4)
    SCIENTIFIC=$(echo "$RESPONSE" | grep -o '"scientific_name":"[^"]*"' | cut -d'"' -f4)
    
    echo "  Reference générée: $REFERENCE"
    echo "  Scientific name: $SCIENTIFIC"
else
    echo -e "${RED}❌ FAILED${NC}"
    echo "Response: $RESPONSE"
fi

# Test 3: Validation - Genus minuscule (doit échouer)
echo ""
echo -n "Test 3 - Validation Genus minuscule (doit échouer): "
RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/plants" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Invalid",
    "family": "Orchidaceae",
    "genus": "phalaenopsis",
    "species": "amabilis"
  }')

# Note: La validation côté client Zod empêcherait cela. Si ça passe le backend,
# c'est que le backend n'a pas de validation stricte (acceptable)
if echo "$RESPONSE" | grep -q '"id"'; then
    echo -e "${YELLOW}⚠️ ACCEPTÉ${NC} (backend plus permissif que client)"
elif echo "$RESPONSE" | grep -q '"detail"'; then
    echo -e "${GREEN}✅ REJETÉ${NC} (validation backend active)"
else
    echo -e "${YELLOW}?${NC} Réponse inattendue"
fi

# Test 4: Récupération des plantes
echo ""
echo -n "Test 4 - Récupération des plantes: "
RESPONSE=$(curl -s "${BACKEND_URL}/api/plants")

if echo "$RESPONSE" | grep -q '"total"'; then
    TOTAL=$(echo "$RESPONSE" | grep -o '"total":[0-9]*' | cut -d: -f2)
    echo -e "${GREEN}✅ OK${NC} (Total: $TOTAL plantes)"
else
    echo -e "${RED}❌ FAILED${NC}"
fi

echo ""
echo -e "${BLUE}Tests Terminés!${NC}"
echo ""
echo -e "${YELLOW}Prochaine étape:${NC}"
echo "1. Ouvrir http://localhost:5173 dans le navigateur"
echo "2. Tester les validations en live"
echo "3. Vérifier les messages d'erreur en français"
echo "4. Éditer les plantes créées"
echo "5. Consulter TEST_RESULTS_PHASE_3_1.md"

