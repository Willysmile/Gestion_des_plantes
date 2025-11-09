#!/bin/bash

# Script pour télécharger des vraies photos de plantes depuis Wikimedia Commons
# Utilise des URLs Wikimedia qui fonctionnent sans restrictions

PHOTOS_DIR="/home/willysmile/Documents/Gestion_des_plantes/data/photos"
DB_PATH="/home/willysmile/Documents/Gestion_des_plantes/data/plants.db"

# Créer le répertoire s'il n'existe pas
mkdir -p "$PHOTOS_DIR"

# Tableau associatif avec les IDs des plantes et leurs URLs Wikimedia
declare -A PLANT_URLS=(
    [1]="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Monstera_deliciosa.jpg/640px-Monstera_deliciosa.jpg"  # Monstera Deliciosa
    [2]="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Pothos_plant.jpg/640px-Pothos_plant.jpg"  # Pothos
    [3]="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Spathiphyllum_wallisii.jpg/640px-Spathiphyllum_wallisii.jpg"  # Spathiphyllum
    [4]="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Sansevieria_trifasciata.jpg/640px-Sansevieria_trifasciata.jpg"  # Sansevieria
    [5]="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/ZZ_plant_%28Zamioculcas_zamiifolia%29.jpg/640px-ZZ_plant_%28Zamioculcas_zamiifolia%29.jpg"  # ZZ Plant
    [6]="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Philodendron_hederaceum.jpg/640px-Philodendron_hederaceum.jpg"  # Philodendron Hederaceum
    [7]="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Dracaena_marginata.jpg/640px-Dracaena_marginata.jpg"  # Dracaena Marginata
    [8]="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Ficus_elastica.jpg/640px-Ficus_elastica.jpg"  # Ficus Elastica
    [9]="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Calathea_zebrina.jpg/640px-Calathea_zebrina.jpg"  # Calathea
    [10]="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Scindapsus_pictus.jpg/640px-Scindapsus_pictus.jpg"  # Scindapsus
    [11]="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Alocasia_amazonica.jpg/640px-Alocasia_amazonica.jpg"  # Alocasia
    [12]="https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Anthurium_andraeanum.jpg/640px-Anthurium_andraeanum.jpg"  # Anthurium
    [13]="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Monstera_deliciosa_variegata.jpg/640px-Monstera_deliciosa_variegata.jpg"  # Monstera Variegata
    [14]="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Epipremnum_pinnatum.jpg/640px-Epipremnum_pinnatum.jpg"  # Epipremnum
    [15]="https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Ficus_lyrata.jpg/640px-Ficus_lyrata.jpg"  # Ficus Lyrata
    [16]="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Rhaphidophora_tetrasperma.jpg/640px-Rhaphidophora_tetrasperma.jpg"  # Rhaphidophora
    [17]="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Peperomia_obtusifolia.jpg/640px-Peperomia_obtusifolia.jpg"  # Peperomia
    [18]="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Pilea_peperomioides.jpg/640px-Pilea_peperomioides.jpg"  # Pilea
    [19]="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Adenium_obesum.jpg/640px-Adenium_obesum.jpg"  # Adenium
    [20]="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Lithops_living_stones.jpg/640px-Lithops_living_stones.jpg"  # Lithops
    [21]="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Stapelia_variegata.jpg/640px-Stapelia_variegata.jpg"  # Stapelia
    [22]="https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Crassula_ovata.jpg/640px-Crassula_ovata.jpg"  # Crassula
)

echo "📥 Téléchargement des photos de plantes..."
echo "========================================="

for plant_id in "${!PLANT_URLS[@]}"; do
    url="${PLANT_URLS[$plant_id]}"
    filename="plant_${plant_id}_photo1.jpg"
    filepath="$PHOTOS_DIR/$filename"
    
    echo -n "[$plant_id/22] Téléchargement de $filename... "
    
    # Télécharger avec curl et redirection
    if curl -s -L -o "$filepath" "$url" 2>/dev/null; then
        # Vérifier que le fichier a du contenu
        if [ -s "$filepath" ]; then
            file_size=$(stat -f%z "$filepath" 2>/dev/null || stat -c%s "$filepath" 2>/dev/null)
            echo "✅ ($file_size bytes)"
            
            # Insérer dans la BD avec is_primary=1
            sqlite3 "$DB_PATH" "INSERT INTO photos (plant_id, filename, file_size, width, height, is_primary, created_at, updated_at) VALUES ($plant_id, '$filename', $file_size, 400, 400, 1, datetime('now'), datetime('now'));"
        else
            echo "❌ Fichier vide"
            rm -f "$filepath"
        fi
    else
        echo "❌ Erreur réseau"
    fi
done

echo ""
echo "========================================="
echo "📊 Résumé:"
echo "Photos téléchargées: $(ls -1 $PHOTOS_DIR/*.jpg 2>/dev/null | wc -l)"
echo "Photos en BD: $(sqlite3 $DB_PATH 'SELECT COUNT(*) FROM photos;')"
