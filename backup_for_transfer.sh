#!/bin/bash

# Script de backup pour transfert vers autre PC
# Usage: ./backup_for_transfer.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BACKUP_DIR="$HOME/Desktop/gestion_plantes_backup_$(date +%Y%m%d_%H%M%S)"
ARCHIVE_NAME="gestion_plantes_backup_$(date +%Y%m%d_%H%M%S).tar.gz"

echo "🚀 Backup Gestion des Plantes"
echo "=============================="
echo ""

# Créer dossier temporaire
echo "📁 Création dossier backup..."
mkdir -p "$BACKUP_DIR"

# Copier code source (sans dépendances)
echo "📦 Copie code source..."
rsync -av \
  --exclude='backend/venv' \
  --exclude='frontend/node_modules' \
  --exclude='backend/**/__pycache__' \
  --exclude='frontend/dist' \
  --exclude='frontend/.vite' \
  --exclude='.git' \
  --exclude='*.pyc' \
  --exclude='*.log' \
  ./ "$BACKUP_DIR/"

# Créer archive data séparée
echo "💾 Archive base de données et photos..."
if [ -d "backend/data" ]; then
  tar -czf "$BACKUP_DIR/data_backup.tar.gz" \
    -C backend data/
  echo "  ✓ data_backup.tar.gz créé"
fi

# Copier documentation importante
echo "📄 Copie documentation..."
cp -f README_TRANSFERT.md "$BACKUP_DIR/" 2>/dev/null || true
cp -f INSTALLATION_NOUVEAU_PC.md "$BACKUP_DIR/" 2>/dev/null || true
cp -f SYNC_AVEC_AUTRE_PC.md "$BACKUP_DIR/" 2>/dev/null || true

# Créer fichier info
cat > "$BACKUP_DIR/BACKUP_INFO.txt" << EOF
===========================================
BACKUP GESTION DES PLANTES
===========================================

Date: $(date '+%Y-%m-%d %H:%M:%S')
Branche Git: $(git branch --show-current 2>/dev/null || echo "N/A")
Dernier commit: $(git log -1 --oneline 2>/dev/null || echo "N/A")

CONTENU:
--------
1. Code source complet (sans node_modules/venv)
2. data_backup.tar.gz - Base de données + photos
3. Documentation installation

INSTALLATION SUR AUTRE PC:
--------------------------
1. Extraire cette archive
2. Lire README_TRANSFERT.md
3. Suivre INSTALLATION_NOUVEAU_PC.md

RESTAURER DONNÉES:
------------------
cd backend
tar -xzf ../data_backup.tar.gz

PRÉREQUIS:
----------
- Python 3.11+
- Node.js 18+
- Git

Contact: Gestion des Plantes v2.0
===========================================
EOF

echo "  ✓ BACKUP_INFO.txt créé"

# Créer archive finale
echo "🗜️  Compression archive finale..."
cd "$HOME/Desktop"
tar -czf "$ARCHIVE_NAME" "$(basename "$BACKUP_DIR")"

# Nettoyer dossier temporaire
rm -rf "$BACKUP_DIR"

# Afficher résumé
ARCHIVE_SIZE=$(du -h "$HOME/Desktop/$ARCHIVE_NAME" | cut -f1)

echo ""
echo "✅ BACKUP TERMINÉ !"
echo "=================="
echo ""
echo "📦 Archive: $HOME/Desktop/$ARCHIVE_NAME"
echo "📊 Taille: $ARCHIVE_SIZE"
echo ""
echo "🚀 PROCHAINES ÉTAPES:"
echo "  1. Copier l'archive sur USB/réseau"
echo "  2. Sur l'autre PC, extraire:"
echo "     tar -xzf $ARCHIVE_NAME"
echo "  3. Suivre INSTALLATION_NOUVEAU_PC.md"
echo ""
echo "💡 ASTUCE: Pour voir le contenu sans extraire:"
echo "   tar -tzf $ARCHIVE_NAME | head -20"
echo ""
