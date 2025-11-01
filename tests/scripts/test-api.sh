#!/bin/bash

# Test script to validate the refactored form
# This tests the actual API endpoints

echo "🧪 Testing Temperature & Humidity Validation..."
echo ""

# Test 1: Create plant with invalid temperatures (min > max)
echo "Test 1: Create plant with temperature_min > temperature_max"
curl -s -X POST http://localhost:8001/api/plants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Plant 1",
    "family": "TestFamily",
    "temperature_min": 30,
    "temperature_max": 20,
    "humidity_level": 60
  }' | jq '.detail' 2>/dev/null || echo "Error in test 1"

echo ""
echo "Test 2: Create plant with humidity_level > 100"
curl -s -X POST http://localhost:8001/api/plants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Plant 2",
    "family": "TestFamily",
    "temperature_min": 15,
    "temperature_max": 25,
    "humidity_level": 120
  }' | jq '.detail' 2>/dev/null || echo "Error in test 2"

echo ""
echo "Test 3: Create plant with valid values"
curl -s -X POST http://localhost:8001/api/plants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Valid Test Plant",
    "family": "TestFamily",
    "temperature_min": 15,
    "temperature_max": 25,
    "humidity_level": 60
  }' | jq '.id, .name, .temperature_min, .temperature_max, .humidity_level' 2>/dev/null || echo "Error in test 3"

echo ""
echo "✅ Tests completed"
