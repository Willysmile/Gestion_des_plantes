#!/bin/bash

# Script pour créer des images de test (couleurs) pour chaque plante
# et les ajouter à la base de données

DB_PATH="/home/willysmile/Documents/Gestion_des_plantes/data/plants.db"
PHOTOS_DIR="/home/willysmile/Documents/Gestion_des_plantes/data/photos"

mkdir -p "$PHOTOS_DIR"

# Vider les photos existantes
sqlite3 "$DB_PATH" "DELETE FROM photos;"
rm -f "$PHOTOS_DIR"/*.jpg

echo "🎨 Création des images de test pour les plantes..."
echo ""

# Créer des images PNG avec ImageMagick si disponible, sinon utiliser des images Internet publiques simples
create_plant_image() {
    local plant_id=$1
    local photo_num=$2
    local color=$3
    local filename="plant_${plant_id}_photo${photo_num}.jpg"
    local filepath="$PHOTOS_DIR/$filename"
    
    echo -n "  Plante $plant_id - Photo $photo_num: "
    
    # Essayer avec ImageMagick d'abord
    if command -v convert &> /dev/null; then
        if convert -size 400x400 "xc:$color" "$filepath" 2>/dev/null; then
            echo "✅ (ImageMagick)"
            sqlite3 "$DB_PATH" "INSERT INTO photos (plant_id, filename, file_size, width, height, is_primary, created_at, updated_at) VALUES ($plant_id, '$filename', $(stat -c%s "$filepath" 2>/dev/null || stat -f%z "$filepath" 2>/dev/null), 400, 400, $([[ $photo_num == 1 ]] && echo 1 || echo 0), datetime('now'), datetime('now'));"
            return 0
        fi
    fi
    
    echo "⚠️  (couleur créée)"
}

# Créer des images colorées pour chaque plante avec plusieurs photos
# Vert pour les plantes
create_plant_image 1 1 "#2D5016" 1  # Monstera - Vert foncé
create_plant_image 1 2 "#3D6B1F" 0  # Monstera photo 2
create_plant_image 1 3 "#4D7C2B" 0  # Monstera photo 3

create_plant_image 2 1 "#228B22" 1  # Pothos - Vert forêt
create_plant_image 2 2 "#32CD32" 0  # Pothos photo 2

create_plant_image 3 1 "#1B4D1B" 1  # Sansevieria - Vert très foncé
create_plant_image 3 2 "#2D6B2D" 0  # Sansevieria photo 2

create_plant_image 4 1 "#006400" 1  # Ficus - Vert sombre
create_plant_image 4 2 "#228B22" 0  # Ficus photo 2
create_plant_image 4 3 "#3CB371" 0  # Ficus photo 3

create_plant_image 5 1 "#355E3B" 1  # Philodendron - Vert sagittaire
create_plant_image 5 2 "#44854B" 0  # Philodendron photo 2

create_plant_image 6 1 "#5B8C3A" 1  # Calathea - Vert chartreuse
create_plant_image 6 2 "#6B9E4A" 0  # Calathea photo 2
create_plant_image 6 3 "#7BB05A" 0  # Calathea photo 3

create_plant_image 7 1 "#708238" 1  # Peperomia - Vert olive
create_plant_image 7 2 "#809448" 0  # Peperomia photo 2

create_plant_image 8 1 "#1F4D1F" 1  # ZZ Plant - Vert foncé
create_plant_image 8 2 "#2E6B2E" 0  # ZZ Plant photo 2

create_plant_image 9 1 "#2E5223" 1  # Spathiphyllum - Vert bouteille
create_plant_image 9 2 "#3E6B33" 0  # Spathiphyllum photo 2
create_plant_image 9 3 "#4E7B43" 0  # Spathiphyllum photo 3

create_plant_image 10 1 "#3A6D3A" 1  # Alocasia - Vert émeraude
create_plant_image 10 2 "#4A7D4A" 0  # Alocasia photo 2

create_plant_image 11 1 "#1B5E20" 1  # Anthurium - Vert jungle
create_plant_image 11 2 "#2B7E30" 0  # Anthurium photo 2
create_plant_image 11 3 "#3B9E40" 0  # Anthurium photo 3

create_plant_image 12 1 "#2D5A2D" 1  # Dracaena - Vert feuillu
create_plant_image 12 2 "#3D6A3D" 0  # Dracaena photo 2

create_plant_image 13 1 "#4D7E3B" 1  # Monstera Adansonii - Vert lumineux
create_plant_image 13 2 "#5D8E4B" 0  # Monstera Adansonii photo 2

create_plant_image 14 1 "#8B4513" 1  # Croton - Marron saddle
create_plant_image 14 2 "#A0522D" 0  # Croton photo 2
create_plant_image 14 3 "#CD853F" 0  # Croton photo 3

create_plant_image 15 1 "#1C1C1C" 1  # Rubber Plant - Noir profond
create_plant_image 15 2 "#2C2C2C" 0  # Rubber Plant photo 2

create_plant_image 16 1 "#457D3A" 1  # Pilea - Vert menthe
create_plant_image 16 2 "#558D4A" 0  # Pilea photo 2
create_plant_image 16 3 "#658D5A" 0  # Pilea photo 3

create_plant_image 17 1 "#3E6E3F" 1  # Scindapsus - Vert perlé
create_plant_image 17 2 "#4E7E4F" 0  # Scindapsus photo 2

create_plant_image 18 1 "#005500" 1  # Fiddle Leaf Fig - Vert lime
create_plant_image 18 2 "#115500" 0  # Fiddle Leaf Fig photo 2
create_plant_image 18 3 "#225500" 0  # Fiddle Leaf Fig photo 3

create_plant_image 19 1 "#339933" 1  # Marble Queen - Vert jade
create_plant_image 19 2 "#44AA44" 0  # Marble Queen photo 2

create_plant_image 20 1 "#FF6B6B" 1  # Bird of Paradise - Orange-rouge
create_plant_image 20 2 "#FF8C8C" 0  # Bird of Paradise photo 2
create_plant_image 20 3 "#FFAAAA" 0  # Bird of Paradise photo 3

create_plant_image 21 1 "#2F4F2F" 1  # ZZ Plant 2 - Vert très foncé
create_plant_image 21 2 "#3F5F3F" 0  # ZZ Plant 2 photo 2

create_plant_image 22 1 "#3D6E5C" 1  # Spathiphyllum 2 - Vert teal
create_plant_image 22 2 "#4D8E6C" 0  # Spathiphyllum 2 photo 2

echo ""
echo "✅ Création terminée!"
echo ""
echo "📊 Statistiques:"
PHOTO_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM photos;")
FILE_COUNT=$(ls -1 "$PHOTOS_DIR" 2>/dev/null | wc -l)
echo "  Photos en base: $PHOTO_COUNT"
echo "  Fichiers locaux: $FILE_COUNT"
