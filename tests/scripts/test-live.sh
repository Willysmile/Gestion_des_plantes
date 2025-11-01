#!/bin/bash

# Test complet backend + frontend

echo "════════════════════════════════════════════════"
echo "🧪 TEST SERVEURS - PHASE 3.2 PHOTO GALLERY"
echo "════════════════════════════════════════════════"
echo ""

# Test 1: Backend Health Check
echo "🔍 Test 1: Backend Health Check"
echo "URL: http://localhost:8001/api/plants"
echo ""

response=$(timeout 5 curl -s -w "\n%{http_code}" http://localhost:8001/api/plants 2>/dev/null)
status=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$status" = "200" ]; then
    echo "✅ Backend responding (HTTP 200)"
    # Count plants
    plant_count=$(echo "$body" | grep -o '"id"' | wc -l)
    echo "   Found $plant_count plants"
else
    echo "❌ Backend error (HTTP $status)"
fi
echo ""

# Test 2: Frontend Health Check
echo "🔍 Test 2: Frontend Health Check"
echo "URL: http://localhost:5173"
echo ""

response=$(timeout 5 curl -s -w "\n%{http_code}" http://localhost:5173 2>/dev/null)
status=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$status" = "200" ]; then
    echo "✅ Frontend responding (HTTP 200)"
    # Check for React app marker
    if echo "$body" | grep -q "react\|root\|App"; then
        echo "   React app loaded successfully"
    fi
else
    echo "❌ Frontend error (HTTP $status)"
fi
echo ""

# Test 3: API Endpoints
echo "🔍 Test 3: Key API Endpoints"
echo ""

endpoints=(
    "/api/plants|GET plants list"
    "/api/lookups/locations|GET locations"
    "/api/lookups/watering-frequencies|GET watering frequencies"
)

for endpoint in "${endpoints[@]}"; do
    path=$(echo $endpoint | cut -d'|' -f1)
    name=$(echo $endpoint | cut -d'|' -f2)
    
    status=$(timeout 3 curl -s -o /dev/null -w "%{http_code}" http://localhost:8001${path} 2>/dev/null)
    
    if [ "$status" = "200" ]; then
        echo "✅ $name (HTTP $status)"
    else
        echo "❌ $name (HTTP $status)"
    fi
done
echo ""

# Test 4: Process Status
echo "🔍 Test 4: Process Status"
echo ""

backend_pid=$(ps aux | grep "uvicorn app.main" | grep -v grep | awk '{print $2}')
frontend_pid=$(ps aux | grep "npm run dev" | grep -v grep | awk '{print $2}')

if [ -n "$backend_pid" ]; then
    echo "✅ Backend process running (PID: $backend_pid)"
else
    echo "❌ Backend process not running"
fi

if [ -n "$frontend_pid" ]; then
    echo "✅ Frontend process running (PID: $frontend_pid)"
else
    echo "❌ Frontend process not running"
fi
echo ""

# Summary
echo "════════════════════════════════════════════════"
echo "✨ TEST SUMMARY"
echo "════════════════════════════════════════════════"
echo ""
echo "🌐 Frontend (Vite):  http://localhost:5173"
echo "🔌 Backend (FastAPI): http://localhost:8001"
echo ""
echo "✅ Ready for live testing!"
echo ""
