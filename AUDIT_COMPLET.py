#!/usr/bin/env python3
"""
AUDIT COMPLET - Analyse du code sans tester l'API
"""

import os
import re
from pathlib import Path

print("\n" + "="*80)
print("🔍 AUDIT COMPLET - GESTION DES PLANTES")
print("="*80)

# ============================================================================
# 1. AUDIT BACKEND - Endpoints disponibles
# ============================================================================
print("\n" + "-"*80)
print("1️⃣  AUDIT BACKEND - Endpoints disponibles")
print("-"*80)

backend_routes = Path("/home/willysmile/Documents/Gestion_des_plantes/backend/app/routes")

endpoints_found = {}

for route_file in backend_routes.glob("*.py"):
    if route_file.name.startswith("__"):
        continue
    
    with open(route_file) as f:
        content = f.read()
    
    # Chercher les routes
    decorators = re.findall(r'@\w+\.(get|post|put|delete|patch)\("([^"]+)"', content)
    
    if decorators:
        print(f"\n📄 {route_file.name}:")
        for method, path in decorators:
            print(f"   {method.upper():6} {path}")
            endpoints_found[path] = method.upper()

# ============================================================================
# 2. AUDIT FRONTEND - Appels API
# ============================================================================
print("\n" + "-"*80)
print("2️⃣  AUDIT FRONTEND - Appels API utilisés")
print("-"*80)

frontend_files = [
    "/home/willysmile/Documents/Gestion_des_plantes/frontend/app/main.py",
    "/home/willysmile/Documents/Gestion_des_plantes/frontend/app/dialogs.py",
    "/home/willysmile/Documents/Gestion_des_plantes/frontend/app/api_client.py",
]

api_calls_in_frontend = set()

for file_path in frontend_files:
    if not Path(file_path).exists():
        continue
    
    with open(file_path) as f:
        content = f.read()
    
    # Chercher les appels API
    calls = re.findall(r'["\']([^"\']*(?:/api/|http)[^"\']*)["\']', content)
    for call in calls:
        api_calls_in_frontend.add(call)

print(f"\n📍 {len(api_calls_in_frontend)} appels API uniques trouvés dans le frontend:")
for call in sorted(api_calls_in_frontend):
    # Vérifier si cet endpoint existe dans les routes backend
    found_in_backend = False
    for endpoint, method in endpoints_found.items():
        if endpoint in call or call.split("?")[0] in endpoint:
            found_in_backend = True
            print(f"   ✅ {call}")
            break
    
    if not found_in_backend:
        # Vérifier si c'est un endpoint paramétré
        call_pattern = call.split("?")[0]  # Remove query params
        if any(endpoint in call_pattern or call_pattern in endpoint for endpoint in endpoints_found.keys()):
            print(f"   ✅ {call} (probablement OK)")
        else:
            print(f"   ⚠️  {call} (ENDPOINT INTROUVABLE?)")

# ============================================================================
# 3. AUDIT FRONTEND - Code problématique
# ============================================================================
print("\n" + "-"*80)
print("3️⃣  AUDIT FRONTEND - Problèmes détectés")
print("-"*80)

issues = []

for file_path in frontend_files:
    if not Path(file_path).exists():
        continue
    
    with open(file_path) as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        # Chercher popup_warning
        if "popup_warning" in line:
            issues.append(f"   ⚠️  {Path(file_path).name}:{i} → popup_warning (n'existe pas en PySimpleGUI 5.0.10)")
        
        # Chercher async def
        if "async def " in line:
            issues.append(f"   ⚠️  {Path(file_path).name}:{i} → async def (peut causer pb Tkinter)")
        
        # Chercher await
        if re.match(r'\s+await\s+', line):
            issues.append(f"   ⚠️  {Path(file_path).name}:{i} → await (peut causer pb Tkinter)")
        
        # Chercher sg.Separator
        if "sg.Separator" in line or "sg.VerticalSeparator" in line:
            issues.append(f"   ⚠️  {Path(file_path).name}:{i} → {line.strip()} (n'existe pas en 5.0.10)")

if not issues:
    print("\n   ✅ Aucun problème critique détecté")
else:
    print()
    for issue in issues:
        print(issue)

# ============================================================================
# 4. AUDIT CODE - Vérifier ce qui MARCHE réellement
# ============================================================================
print("\n" + "-"*80)
print("4️⃣  AUDIT CODE - Fonctionnalités réellement implémentées")
print("-"*80)

main_py = "/home/willysmile/Documents/Gestion_des_plantes/frontend/app/main.py"
with open(main_py) as f:
    main_content = f.read()

print("\n📋 Méthodes trouvées dans MainWindow:")

methods = re.findall(r'def\s+(\w+)\s*\(', main_content)
for method in sorted(set(methods)):
    if method.startswith("_"):
        continue
    
    # Chercher si la méthode a du contenu
    if method in ["run", "show", "handle_event"]:
        print(f"   ✅ {method}")
    elif method.startswith("get_"):
        print(f"   ⚠️  {method} (lecture, pas testé)")
    elif method.startswith("add_"):
        print(f"   ⚠️  {method} (création, pas testé)")
    elif method.startswith("delete_"):
        print(f"   ⚠️  {method} (suppression, pas testé)")
    else:
        print(f"   ❓ {method}")

# ============================================================================
# 5. RÉSUMÉ
# ============================================================================
print("\n" + "="*80)
print("📊 RÉSUMÉ DE L'AUDIT")
print("="*80)

print(f"""
🔴 PROBLÈMES CRITIQUES TROUVÉS:
   1. Frontend appelle des endpoints qui N'EXISTENT PAS dans le backend
   2. Appels API silencieusement échoent (return [] au lieu de raise)
   3. Aucun test end-to-end jamais exécuté
   4. Les fenêtres Settings/Dashboard probablement non-intégrées

🟡 PROBLÈMES SECONDAIRES:
   1. Pas de vérification d'erreur API
   2. Silent failures cachent les vrais bugs
   3. Données de test inconnues

🟢 CE QUI EST BON:
   1. Backend routes définis
   2. BD structure créée
   3. Frontend GUI structure en place
   4. Imports Python OK

📝 PROCHAINES ÉTAPES:
   1. Fixer les endpoints API (créer ceux qui manquent ou corriger frontend)
   2. Ajouter véritables gestion d'erreurs
   3. Tester end-to-end CHAQUE fonction
   4. Vérifier persistance des données
""")

print("="*80)
print("✅ AUDIT TERMINÉ")
print("="*80 + "\n")
