#!/bin/bash

# Test delete photo endpoint

# 1. List all plants to get a plant_id
echo "=== Getting plants ==="
PLANTS=$(curl -s http://localhost:8001/api/plants)
echo "$PLANTS" | jq '.[0]'

# Get first plant ID
PLANT_ID=$(echo "$PLANTS" | jq '.[0].id')
echo "Using plant_id: $PLANT_ID"

# 2. List photos for this plant
echo -e "\n=== Getting photos for plant $PLANT_ID ==="
PHOTOS=$(curl -s http://localhost:8001/api/plants/$PLANT_ID/photos)
echo "$PHOTOS" | jq '.[]'

# Get first photo ID
PHOTO_ID=$(echo "$PHOTOS" | jq '.[0].id')
echo "Using photo_id: $PHOTO_ID"

if [ -z "$PHOTO_ID" ] || [ "$PHOTO_ID" == "null" ]; then
    echo "No photos found for plant $PLANT_ID"
    exit 1
fi

# 3. Show files before delete
echo -e "\n=== Files before delete ==="
find /home/willysmile/Documents/Gestion_des_plantes/data/photos/$PLANT_ID -type f 2>/dev/null

# 4. Delete the photo
echo -e "\n=== Deleting photo $PHOTO_ID ==="
curl -X DELETE http://localhost:8001/api/plants/$PLANT_ID/photos/$PHOTO_ID -v

# 5. Show files after delete
echo -e "\n=== Files after delete ==="
find /home/willysmile/Documents/Gestion_des_plantes/data/photos/$PLANT_ID -type f 2>/dev/null
