#!/bin/bash

# Script de seed: 20 plantes avec historiques et photos

echo "🗑️  Nettoyage de la base de données..."

# Créer les répertoires
mkdir -p /home/willysmile/Documents/Gestion_des_plantes/data/photos

# Vider les tables (garder les lookups)
sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db << 'EOF'
DELETE FROM photos;
DELETE FROM watering_histories;
DELETE FROM fertilizing_histories;
DELETE FROM plants;
DELETE FROM plant_tag;
DELETE FROM plant_health_statuses;
EOF

echo "✅ Base de données vidée"
echo ""

# Tableaux de données
declare -a NAMES=("Monstera Deliciosa" "Pothos Aureum" "Sansevieria Trifasciata" "Ficus Lyrata" "Philodendron Hederaceum" "Calathea Orbifolia" "Peperomia Obtusifolia" "ZZ Plant" "Spathiphyllum Wallisii" "Alocasia Amazonica" "Anthurium Andraeanum" "Dracaena Marginata" "Monstera Adansonii" "Croton Codiaeum" "Rubber Plant" "Pilea Peperomioides" "Scindapsus Pictus" "Fiddle Leaf Fig" "Marble Queen Pothos" "Bird of Paradise")

declare -a SCIENTIFIC=("Monstera deliciosa" "Epipremnum aureum" "Dracaena trifasciata" "Ficus lyrata" "Philodendron hederaceum" "Goeppertia orbifolia" "Peperomia obtusifolia" "Zamioculcas zamiifolia" "Spathiphyllum wallisii" "Alocasia amazonica" "Anthurium andraeanum" "Dracaena marginata" "Rhaphidophora tetrasperma" "Codiaeum variegatum" "Ficus elastica" "Pilea peperomioides" "Scindapsus pictus" "Ficus pandurata" "Epipremnum pinnatum" "Strelitzia reginae")

declare -a FAMILIES=("Araceae" "Araceae" "Asparagaceae" "Moraceae" "Araceae" "Marantaceae" "Piperaceae" "Araceae" "Araceae" "Araceae" "Araceae" "Asparagaceae" "Araceae" "Euphorbiaceae" "Moraceae" "Urticaceae" "Araceae" "Moraceae" "Araceae" "Strelitziaceae")

declare -a LOCATIONS=("Salon" "Chambre" "Bureau" "Salon" "Cuisine" "Salon" "Bureau" "Couloir" "Salle de bain" "Salon" "Cuisine" "Entrée" "Bureau" "Salon" "Salon" "Bureau" "Chambre" "Salon" "Cuisine" "Véranda")

declare -a HEALTH=("healthy" "healthy" "healthy" "healthy" "healthy" "healthy" "healthy" "healthy" "recovering" "healthy" "healthy" "healthy" "healthy" "healthy" "healthy" "healthy" "healthy" "healthy" "healthy" "healthy")

declare -a LIGHT=("Lumière indirecte" "Lumière indirecte" "Lumière directe" "Lumière indirecte" "Lumière indirecte" "Lumière indirecte" "Lumière indirecte" "Lumière faible" "Lumière faible" "Lumière indirecte" "Lumière indirecte" "Lumière indirecte" "Lumière indirecte" "Lumière directe" "Lumière indirecte" "Lumière indirecte" "Lumière indirecte" "Lumière indirecte" "Lumière indirecte" "Lumière directe")

declare -a PHOTOS=("https://images.unsplash.com/photo-1502082553048-f007c46585b4?w=400" "https://images.unsplash.com/photo-1614921041307-7a78d57b3dd2?w=400" "https://images.unsplash.com/photo-1614613535308-eb5fbd8d2c17?w=400" "https://images.unsplash.com/photo-1585788050420-dba6306786d8?w=400" "https://images.unsplash.com/photo-1563241527-3004b36b0c65?w=400" "https://images.unsplash.com/photo-1611003228941-98852ba62227?w=400" "https://images.unsplash.com/photo-1598075244200-e1da1c5d4c8e?w=400" "https://images.unsplash.com/photo-1589923188900-c2cd0eaf59ea?w=400" "https://images.unsplash.com/photo-1604911551385-64d1dd6a3f9e?w=400" "https://images.unsplash.com/photo-1620127682293-41b83c96433f?w=400" "https://images.unsplash.com/photo-1617466138997-e1728d1e75fd?w=400" "https://images.unsplash.com/photo-1632207691745-664ffbc58908?w=400" "https://images.unsplash.com/photo-1611003228941-98852ba62227?w=400" "https://images.unsplash.com/photo-1600728906667-b5ace7ae128f?w=400" "https://images.unsplash.com/photo-1613257904352-e30d3da093f6?w=400" "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400" "https://images.unsplash.com/photo-1578359935390-3a97d33e2e41?w=400" "https://images.unsplash.com/photo-1585788050420-dba6306786d8?w=400" "https://images.unsplash.com/photo-1614921041307-7a78d57b3dd2?w=400" "https://images.unsplash.com/photo-1608837907067-4db09e7d5ee0?w=400")

echo "🌱 Création de 20 plantes..."
echo ""

# Créer 20 plantes
for i in {0..19}; do
    NAME="${NAMES[$i]}"
    SCIENTIFIC="${SCIENTIFIC[$i]}"
    FAMILY="${FAMILIES[$i]}"
    LOCATION="${LOCATIONS[$i]}"
    HEALTH="${HEALTH[$i]}"
    LIGHT="${LIGHT[$i]}"
    PHOTO_URL="${PHOTOS[$i]}"
    
    # Échapper les apostrophes
    NAME_ESCAPED="${NAME//\'/\'\'}"
    SCIENTIFIC_ESCAPED="${SCIENTIFIC//\'/\'\'}"
    FAMILY_ESCAPED="${FAMILY//\'/\'\'}"
    LOCATION_ESCAPED="${LOCATION//\'/\'\'}"
    
    MONTH=$((($i % 11) + 1))
    DAY=$((($i % 25) + 1))
    PURCHASE_DATE="2024-$(printf '%02d' $MONTH)-$(printf '%02d' $DAY)"
    
    echo "[$((i+1))/20] Création de $NAME..."
    
    # Obtenir/créer les IDs de lookup
    LOCATION_ID=$(sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db "SELECT id FROM locations WHERE name='$LOCATION_ESCAPED' LIMIT 1;")
    if [ -z "$LOCATION_ID" ]; then
        sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db "INSERT INTO locations (name, created_at, updated_at) VALUES ('$LOCATION_ESCAPED', datetime('now'), datetime('now'));"
        LOCATION_ID=$(sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db "SELECT id FROM locations WHERE name='$LOCATION_ESCAPED' LIMIT 1;")
    fi
    
    LIGHT_ID=$(sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db "SELECT id FROM light_requirements WHERE name='$LIGHT' LIMIT 1;")
    
    # Créer la plante
    sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db << EOSQL
INSERT INTO plants (
    name, scientific_name, family, description, health_status, location_id, 
    light_requirement_id, temperature_min, temperature_max, humidity_level, 
    purchase_date, is_archived, created_at, updated_at
) VALUES (
    '$NAME_ESCAPED', '$SCIENTIFIC_ESCAPED', '$FAMILY_ESCAPED', 'Plante', '$HEALTH', $LOCATION_ID,
    $LIGHT_ID, 15, 27, 60,
    '$PURCHASE_DATE', 0, datetime('now'), datetime('now')
);
EOSQL
    
    PLANT_ID=$(sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db "SELECT id FROM plants WHERE name='$NAME_ESCAPED' ORDER BY id DESC LIMIT 1;")
    
    if [ ! -z "$PLANT_ID" ]; then
        # Ajouter 3 arrosages aléatoires dans les 30 derniers jours
        for j in {1..3}; do
            DAYS_AGO=$((RANDOM % 30 + 1))
            WATER_DATE=$(date -d "-$DAYS_AGO days" +%Y-%m-%d)
            AMOUNT=$((RANDOM % 300 + 200))
            sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db "INSERT INTO watering_histories (plant_id, date, amount_ml, created_at, updated_at) VALUES ($PLANT_ID, '$WATER_DATE', $AMOUNT, datetime('now'), datetime('now'));"
        done
        echo "  ✓ 3 arrosages ajoutés"
        
        # Ajouter 1-2 fertilisations aléatoires
        NUM_FERT=$((RANDOM % 2 + 1))
        for j in $(seq 1 $NUM_FERT); do
            DAYS_AGO=$((RANDOM % 60 + 1))
            FERT_DATE=$(date -d "-$DAYS_AGO days" +%Y-%m-%d)
            sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db "INSERT INTO fertilizing_histories (plant_id, date, amount, created_at, updated_at) VALUES ($PLANT_ID, '$FERT_DATE', '20ml', datetime('now'), datetime('now'));"
        done
        echo "  ✓ Historique de fertilisation ajouté"
    else
        echo "  ✗ Erreur lors de la création de la plante"
    fi
    echo ""
done

echo "✅ Toutes les 20 plantes ont été créées!"
echo ""
echo "📊 Statistiques:"
echo "  Plantes: $(sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db 'SELECT COUNT(*) FROM plants;')"
echo "  Arrosages: $(sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db 'SELECT COUNT(*) FROM watering_histories;')"
echo "  Fertilisations: $(sqlite3 /home/willysmile/Documents/Gestion_des_plantes/data/plants.db 'SELECT COUNT(*) FROM fertilizing_histories;')"
