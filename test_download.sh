#!/bin/bash

# Test simple de téléchargement
PHOTOS_DIR="/home/willysmile/Documents/Gestion_des_plantes/data/photos"
mkdir -p "$PHOTOS_DIR"

echo "Test 1: Wikimedia"
wget -q -O "$PHOTOS_DIR/test1.jpg" "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Monstera_deliciosa001.jpg/640px-Monstera_deliciosa001.jpg" 2>&1
echo "Résultat: $(ls -lh "$PHOTOS_DIR/test1.jpg" 2>&1 | awk '{print $5}')"

echo ""
echo "Test 2: Pexels API"
wget -q -O "$PHOTOS_DIR/test2.jpg" "https://images.pexels.com/photos/5632679/pexels-photo-5632679.jpeg?auto=compress&cs=tinysrgb&w=400" 2>&1
echo "Résultat: $(ls -lh "$PHOTOS_DIR/test2.jpg" 2>&1 | awk '{print $5}')"

echo ""
echo "Test 3: Pixabay"
wget -q -O "$PHOTOS_DIR/test3.jpg" "https://pixabay.com/get/g37d27a57eb5c09f56b6e8a71b5fc9eaea4e66f27ce7c9c893fa87f4f0c2cf4f22_640.jpg" 2>&1
echo "Résultat: $(ls -lh "$PHOTOS_DIR/test3.jpg" 2>&1 | awk '{print $5}')"

rm -f "$PHOTOS_DIR/test*"
