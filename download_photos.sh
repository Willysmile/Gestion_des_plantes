#!/bin/bash

DB_PATH="/home/willysmile/Documents/Gestion_des_plantes/data/plants.db"
PHOTOS_DIR="/home/willysmile/Documents/Gestion_des_plantes/data/photos"

mkdir -p "$PHOTOS_DIR"

# Vider les photos existantes
sqlite3 "$DB_PATH" "DELETE FROM photos;"
rm -f "$PHOTOS_DIR"/*

echo "📸 Téléchargement des vraies photos..."
echo ""

# Fonction pour télécharger une photo
download_photo() {
    local plant_id=$1
    local photo_num=$2
    local url=$3
    local is_primary=$4
    
    local filename="plant_${plant_id}_photo${photo_num}.jpg"
    local filepath="$PHOTOS_DIR/$filename"
    
    echo -n "  Plante $plant_id - Photo $photo_num: "
    
    # Télécharger avec wget
    if wget -q -O "$filepath" "$url" 2>/dev/null && [ -s "$filepath" ]; then
        local file_size=$(stat -c%s "$filepath" 2>/dev/null || stat -f%z "$filepath" 2>/dev/null || echo 0)
        
        # Vérifier que ce n'est pas un fichier vide ou trop petit
        if [ "$file_size" -gt 2000 ]; then
            sqlite3 "$DB_PATH" "INSERT INTO photos (plant_id, filename, file_size, width, height, is_primary, created_at, updated_at) VALUES ($plant_id, '$filename', $file_size, 400, 400, $is_primary, datetime('now'), datetime('now'));"
            echo "✅ ($file_size bytes)"
            return 0
        fi
    fi
    
    echo "❌"
    rm -f "$filepath" 2>/dev/null
    return 1
}

# Photos réelles de plantes (Wikimedia, Pixabay, etc.)
# Plante 1: Monstera Deliciosa - 3 photos
download_photo 1 1 "https://upload.wikimedia.org/wikipedia/commons/f/f1/Monstera_deliciosa001.jpg" 1
download_photo 1 2 "https://upload.wikimedia.org/wikipedia/commons/1/1c/Monstera_deliciosa_fleur.jpg" 0
download_photo 1 3 "https://upload.wikimedia.org/wikipedia/commons/8/8f/Monstera_Deliciosa.jpg" 0

# Plante 2: Pothos - 2 photos
download_photo 2 1 "https://upload.wikimedia.org/wikipedia/commons/d/d4/Epipremnum_pinnatum.jpg" 1
download_photo 2 2 "https://upload.wikimedia.org/wikipedia/commons/e/ef/Epipremnum_aureum_-_Money_Plant.jpg" 0

# Plante 3: Sansevieria - 2 photos
download_photo 3 1 "https://upload.wikimedia.org/wikipedia/commons/f/f9/Sansevieria_trifasciata_-_snake_plant.jpg" 1
download_photo 3 2 "https://upload.wikimedia.org/wikipedia/commons/6/64/Sansevieria_cylindrica.jpg" 0

# Plante 4: Ficus Lyrata - 3 photos
download_photo 4 1 "https://upload.wikimedia.org/wikipedia/commons/d/da/Ficus_lyrata_0.jpg" 1
download_photo 4 2 "https://upload.wikimedia.org/wikipedia/commons/5/54/Ficus_lyrata.jpg" 0
download_photo 4 3 "https://upload.wikimedia.org/wikipedia/commons/9/95/Ficus_lyrata_close-up.jpg" 0

# Plante 5: Philodendron - 2 photos
download_photo 5 1 "https://upload.wikimedia.org/wikipedia/commons/0/0d/Philodendron_hederaceum_02.jpg" 1
download_photo 5 2 "https://upload.wikimedia.org/wikipedia/commons/8/8e/Philodendron_hederaceum.jpg" 0

# Plante 6: Calathea - 3 photos
download_photo 6 1 "https://upload.wikimedia.org/wikipedia/commons/b/b6/Calathea_orbifolia.jpg" 1
download_photo 6 2 "https://upload.wikimedia.org/wikipedia/commons/a/a8/Calathea_rotundifolia.jpg" 0
download_photo 6 3 "https://upload.wikimedia.org/wikipedia/commons/3/3d/Calathea_crocata.jpg" 0

# Plante 7: Peperomia - 2 photos
download_photo 7 1 "https://upload.wikimedia.org/wikipedia/commons/4/43/Peperomia_obtusifolia_rubella.jpg" 1
download_photo 7 2 "https://upload.wikimedia.org/wikipedia/commons/2/27/Peperomia_obtusifolia.jpg" 0

# Plante 8: ZZ Plant - 2 photos
download_photo 8 1 "https://upload.wikimedia.org/wikipedia/commons/8/82/Zamioculcas_zamiifolia_001.jpg" 1
download_photo 8 2 "https://upload.wikimedia.org/wikipedia/commons/f/f3/Zamioculcas_zamiifolia.jpg" 0

# Plante 9: Spathiphyllum - 3 photos
download_photo 9 1 "https://upload.wikimedia.org/wikipedia/commons/8/8a/Spathiphyllum_wallisii.jpg" 1
download_photo 9 2 "https://upload.wikimedia.org/wikipedia/commons/c/c4/Spathiphyllum_wallisii_002.jpg" 0
download_photo 9 3 "https://upload.wikimedia.org/wikipedia/commons/e/eb/Spathiphyllum.jpg" 0

# Plante 10: Alocasia - 2 photos
download_photo 10 1 "https://upload.wikimedia.org/wikipedia/commons/d/d3/Alocasia_amazonica.jpg" 1
download_photo 10 2 "https://upload.wikimedia.org/wikipedia/commons/0/0c/Alocasia_polly.jpg" 0

# Plante 11: Anthurium - 3 photos
download_photo 11 1 "https://upload.wikimedia.org/wikipedia/commons/2/2e/Anthurium_andraeanum.jpg" 1
download_photo 11 2 "https://upload.wikimedia.org/wikipedia/commons/1/1d/Anthurium_andraeanum_-_flamingo_flower.jpg" 0
download_photo 11 3 "https://upload.wikimedia.org/wikipedia/commons/8/8c/Anthurium.jpg" 0

# Plante 12: Dracaena - 2 photos
download_photo 12 1 "https://upload.wikimedia.org/wikipedia/commons/6/67/Dracaena_marginata.jpg" 1
download_photo 12 2 "https://upload.wikimedia.org/wikipedia/commons/f/f9/Dracaena_marginata_001.jpg" 0

# Plante 13: Monstera Adansonii - 2 photos
download_photo 13 1 "https://upload.wikimedia.org/wikipedia/commons/1/1a/Rhaphidophora_tetrasperma.jpg" 1
download_photo 13 2 "https://upload.wikimedia.org/wikipedia/commons/9/9e/Monstera_adansonii.jpg" 0

# Plante 14: Croton - 3 photos
download_photo 14 1 "https://upload.wikimedia.org/wikipedia/commons/7/7e/Codiaeum_variegatum.jpg" 1
download_photo 14 2 "https://upload.wikimedia.org/wikipedia/commons/a/a5/Croton_leaf.jpg" 0
download_photo 14 3 "https://upload.wikimedia.org/wikipedia/commons/b/b0/Codiaeum.jpg" 0

# Plante 15: Rubber Plant - 2 photos
download_photo 15 1 "https://upload.wikimedia.org/wikipedia/commons/2/2c/Ficus_elastica_001.jpg" 1
download_photo 15 2 "https://upload.wikimedia.org/wikipedia/commons/e/e6/Ficus_elastica.jpg" 0

# Plante 16: Pilea - 3 photos
download_photo 16 1 "https://upload.wikimedia.org/wikipedia/commons/3/34/Pilea_peperomioides.jpg" 1
download_photo 16 2 "https://upload.wikimedia.org/wikipedia/commons/5/51/Pilea_peperomioides_001.jpg" 0
download_photo 16 3 "https://upload.wikimedia.org/wikipedia/commons/d/de/Chinese_money_plant.jpg" 0

# Plante 17: Scindapsus - 2 photos
download_photo 17 1 "https://upload.wikimedia.org/wikipedia/commons/5/5f/Scindapsus_pictus.jpg" 1
download_photo 17 2 "https://upload.wikimedia.org/wikipedia/commons/a/ab/Satin_pothos.jpg" 0

# Plante 18: Fiddle Leaf Fig - 3 photos
download_photo 18 1 "https://upload.wikimedia.org/wikipedia/commons/8/8f/Ficus_lyrata_001.jpg" 1
download_photo 18 2 "https://upload.wikimedia.org/wikipedia/commons/d/da/Ficus_lyrata_0.jpg" 0
download_photo 18 3 "https://upload.wikimedia.org/wikipedia/commons/9/9e/Ficus_lyrata_leaf.jpg" 0

# Plante 19: Marble Queen Pothos - 2 photos
download_photo 19 1 "https://upload.wikimedia.org/wikipedia/commons/d/d4/Epipremnum_aureum_variegata.jpg" 1
download_photo 19 2 "https://upload.wikimedia.org/wikipedia/commons/e/ef/Epipremnum_aureum.jpg" 0

# Plante 20: Bird of Paradise - 3 photos
download_photo 20 1 "https://upload.wikimedia.org/wikipedia/commons/0/0e/Strelitzia_reginae_004.jpg" 1
download_photo 20 2 "https://upload.wikimedia.org/wikipedia/commons/f/f9/Strelitzia_reginae_-_Strelitzia_-_Queen_of_Flowers_-_Strelizia_2.jpg" 0
download_photo 20 3 "https://upload.wikimedia.org/wikipedia/commons/1/1c/Strelitzia_reginae.jpg" 0

# Plante 21 & 22: Doublons
download_photo 21 1 "https://upload.wikimedia.org/wikipedia/commons/8/82/Zamioculcas_zamiifolia_001.jpg" 1
download_photo 21 2 "https://upload.wikimedia.org/wikipedia/commons/f/f3/Zamioculcas_zamiifolia.jpg" 0

download_photo 22 1 "https://upload.wikimedia.org/wikipedia/commons/8/8a/Spathiphyllum_wallisii.jpg" 1
download_photo 22 2 "https://upload.wikimedia.org/wikipedia/commons/c/c4/Spathiphyllum_wallisii_002.jpg" 0

echo ""
echo "✅ Téléchargement terminé!"
echo ""
echo "📊 Statistiques:"
PHOTO_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM photos;")
FILE_COUNT=$(ls -1 "$PHOTOS_DIR" 2>/dev/null | wc -l)
echo "  Photos en base: $PHOTO_COUNT"
echo "  Fichiers locaux: $FILE_COUNT"
