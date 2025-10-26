#!/bin/bash
# TEST END-TO-END SIMPLE AVEC CURL

echo "======================================================================"
echo "TEST END-TO-END - Gestion des Plantes"
echo "======================================================================"

BASE_URL="http://127.0.0.1:8000"

# TEST 1: Health Check
echo -e "\n✅ TEST 1: Health Check"
curl -s "$BASE_URL/health" | python3 -m json.tool

# TEST 2: Get Plants
echo -e "\n✅ TEST 2: Get all plants"
PLANTS=$(curl -s "$BASE_URL/api/plants")
echo "$PLANTS" | python3 -m json.tool | head -20

# TEST 3: Get Locations
echo -e "\n✅ TEST 3: Get Locations"
curl -s "$BASE_URL/api/settings/locations" | python3 -m json.tool | head -10

# TEST 4: Create Plant
echo -e "\n✅ TEST 4: Create Plant"
NEW_PLANT=$(curl -s -X POST "$BASE_URL/api/plants" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test_Plant_'"$(date +%s)"'",
    "location_id": 1,
    "purchase_place_id": 1,
    "purchase_date": "2025-01-01",
    "watering_frequency_id": 1,
    "light_requirement_id": 1,
    "difficulty_level": "Easy",
    "health_status": "Good"
  }')

echo "$NEW_PLANT" | python3 -m json.tool

# Extract ID
PLANT_ID=$(echo "$NEW_PLANT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
echo "Created Plant ID: $PLANT_ID"

# TEST 5: Get Plant
if [ ! -z "$PLANT_ID" ]; then
  echo -e "\n✅ TEST 5: Get Plant (ID: $PLANT_ID)"
  curl -s "$BASE_URL/api/plants/$PLANT_ID" | python3 -m json.tool
fi

# TEST 6: Update Plant
if [ ! -z "$PLANT_ID" ]; then
  echo -e "\n✅ TEST 6: Update Plant"
  UPDATED=$(curl -s -X PUT "$BASE_URL/api/plants/$PLANT_ID" \
    -H "Content-Type: application/json" \
    -d '{
      "name": "Test_Plant_UPDATED_'"$(date +%s)"'",
      "location_id": 1,
      "purchase_place_id": 1,
      "purchase_date": "2025-01-01",
      "watering_frequency_id": 1,
      "light_requirement_id": 1,
      "difficulty_level": "Medium",
      "health_status": "Excellent"
    }')
  echo "$UPDATED" | python3 -m json.tool
fi

# TEST 7: Get Watering History
if [ ! -z "$PLANT_ID" ]; then
  echo -e "\n✅ TEST 7: Get Watering History"
  curl -s "$BASE_URL/api/plants/$PLANT_ID/watering-history" | python3 -m json.tool
fi

# TEST 8: Delete Plant
if [ ! -z "$PLANT_ID" ]; then
  echo -e "\n✅ TEST 8: Delete Plant"
  DELETE_RESULT=$(curl -s -X DELETE "$BASE_URL/api/plants/$PLANT_ID")
  echo "Delete response: $DELETE_RESULT"
  
  echo -e "\n✅ TEST 9: Verify Deletion (should be 404 or deleted_at set)"
  curl -s "$BASE_URL/api/plants/$PLANT_ID" | python3 -m json.tool || echo "404 - Plant deleted"
fi

echo -e "\n======================================================================"
echo "✅ TESTS COMPLETED"
echo "======================================================================"
