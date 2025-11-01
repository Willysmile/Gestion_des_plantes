#!/bin/bash

# Phase 3.2 - Automated E2E Tests
# Tests: Photo upload, delete, gallery, carousel

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_URL="http://localhost:8001/api"
PLANT_ID=1  # Default test plant ID

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
test_endpoint() {
  local name=$1
  local method=$2
  local endpoint=$3
  local data=$4
  local expected_status=$5

  echo -e "${YELLOW}Testing: $name${NC}"
  
  if [ "$method" = "GET" ]; then
    response=$(curl -s -w "\n%{http_code}" "$API_URL$endpoint")
  elif [ "$method" = "POST" ]; then
    response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" "$API_URL$endpoint")
  elif [ "$method" = "DELETE" ]; then
    response=$(curl -s -w "\n%{http_code}" -X DELETE "$API_URL$endpoint")
  else
    echo -e "${RED}Unknown method: $method${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    return
  fi

  status_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | head -n-1)

  if [ "$status_code" = "$expected_status" ]; then
    echo -e "${GREEN}✓ PASS (HTTP $status_code)${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
  else
    echo -e "${RED}✗ FAIL (Expected $expected_status, got $status_code)${NC}"
    echo "Response: $body"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
  echo ""
}

echo "=========================================="
echo "Phase 3.2 - Photo Gallery E2E Tests"
echo "=========================================="
echo ""

# Test 1: Check if backend is running
echo -e "${YELLOW}Checking backend connectivity...${NC}"
if ! curl -s "$API_URL/plants" > /dev/null 2>&1; then
  echo -e "${RED}✗ Backend not running on $API_URL${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Backend is running${NC}"
echo ""

# Test 2: Get plants list
test_endpoint "Get plants list" "GET" "/plants" "" "200"

# Test 3: Get specific plant
test_endpoint "Get plant details" "GET" "/plants/$PLANT_ID" "" "200"

# Test 4: Get photos list (should be empty or existing)
test_endpoint "Get photos list" "GET" "/plants/$PLANT_ID/photos" "" "200"

# Test 5: Check if data/photos directory exists
echo -e "${YELLOW}Checking data/photos directory...${NC}"
PHOTOS_DIR="/home/willysmile/Documents/Gestion_des_plantes/data/photos/$PLANT_ID"
if [ -d "$PHOTOS_DIR" ]; then
  echo -e "${GREEN}✓ Photos directory exists${NC}"
  echo "  Contents:"
  ls -lh "$PHOTOS_DIR" 2>/dev/null | tail -n +2 | awk '{print "    " $9 " (" $5 ")"}'
else
  echo -e "${YELLOW}Photos directory does not exist yet (will be created on first upload)${NC}"
fi
echo ""

# Test 6: Summary
echo "=========================================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo "=========================================="

if [ $TESTS_FAILED -gt 0 ]; then
  exit 1
fi

echo ""
echo "✓ All automated tests passed!"
echo ""
echo "Next: Manual E2E tests required:"
echo "1. Upload test image via web UI"
echo "2. Verify WebP conversion and file sizes"
echo "3. Test gallery display and carousel"
echo "4. Test delete and set-primary functions"
