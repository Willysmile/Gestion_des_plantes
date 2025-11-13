# Plan de conversion d'une bouture en plante indépendante

> Ce document résume les données issues d'une `PlantPropagation` (bouture) qui peuvent être réutilisées pour créer la nouvelle plante enfant ainsi que les étapes nécessaires avant d'implémenter le bouton "Convert to plant".

## 1. Contrat attendu

- **API existante** : `POST /api/propagations/{propagation_id}/convert` prend un `PropagationConversionRequest` contenant `child_plant_id` (référence vers la plante fille finale) et une `success_date` facultative. La route vérifie l'absence de cycle, met à jour la propagation (`child_plant_id`, `status`, `success_date`) et renvoie la propagation mise à jour.
- **Objectif UX** : proposer un flux qui, depuis la fiche de propagation, permet de :
  1. Visualiser les données accumulées (dates, mesures, notes, événements récents).  
  2. Préremplir un formulaire ou un panneau "Nouvelle plante" avec les informations pertinentes de la propagation et des paramètres hérités (fréquences d'arrosage, emplacement, méthodes).
  3. Valider le passage (statut minimum, absence de conversion déjà effectuée) puis déclencher l'appel API.

## 2. Données issues directement de la propagation à garder

| Champ | Usage dans la plante fille | Remarques | Type cible |
|-------|----------------------------|-----------|------------|
| `source_type`, `method` | Permet d'afficher comment la bouture a été réalisée dans l'historique de la plante fille | Conserver comme métadonnée lecture seule (ex. "Source : cutting · Méthode : water") | chaîne |
| `propagation_date`, `date_harvested`, `expected_ready`, `success_date` | Dates de référence pour le suivi (champ "en propagation" dans la fiche de la plante) | `success_date` peut devenir la `date_planted` | date |
| `status` (p. ex. `rooted`, `ready-to-pot`, `potted`) | Déterminer si la conversion est permise (`potted`/`ready-to-pot`/`established`) et annoter l'historique de la plante | Ne pas écraser `health_status`, mais l'inscrire dans un journal | chaîne |
| `current_root_length_cm`, `current_leaves_count`, `current_roots_count` | Préremplir les mesures d'entrée de la nouvelle plante (par exemple dans le premier `PlantHistory`) | Convertir en `float/int` | nombre |
| `notes` | Copier dans la description initiale ou le premier historique (`PlantHistory` ou `PropagationEvent`) | Peut être ajouté comme note initiale | texte |
| `success_rate_estimate` | Proposer un indicateur de confiance (affiché dans l'interface conversion) | Aussi utile pour analyse | float |
| `events` récents (dernier `PropagationEvent`) | Transférer le dernier événement (type, photo, mesures) en tant qu'événement fondateur de la plante | Fournit un contexte visuel | objet JSON |

> **Rupture de données** : si la propagation n'a pas encore de `child_plant_id`, on la convertit ; si un enfant existe, on propose un lien vers la plante fille et on évite la conversion.

## 3. Renseignements hérités du parent (plant existante)

Lorsqu'on crée la plante fille (par exemple via formulaire `POST /api/plants`), on peut copier :

- **Localisation** : `location_id` (supports greenhouse, orangerie, etc.).
- **Fréquences & méthodes** : `watering_frequency_id`, `preferred_watering_method_id`, `preferred_water_type_id`, `light_requirement_id`.
- **Environnement** : `is_indoor`, `is_outdoor`, `temperature_min`, `temperature_max`, `humidity_level`, `soil_type`, `soil_humidity`, `soil_ideal_ph`, `pot_size`.
- **Tags & classification** : `difficulty_level`, `growth_speed`, `flowering_season` si le parent les définit, afin de maintenir la cohérence de la lignée.
- **Nom** : utiliser un nom explicite (`{parent.name} (Bouture #{propagation.id})` ou champ personnalisé fourni par l'utilisateur). Si un `reference` unique est nécessaire, dériver depuis la propagation (ex. `parent.reference` + `-cutting-{id}`).

Ces valeurs permettront au formulaire de conversion d'afficher un squelette déjà rempli lorsque l'utilisateur choisit d'hériter des réglages parentaux (`inherit_parent_settings`).

## 4. Étapes d'implémentation proposées

1. **Préconditions**
   - Vérifier que la propagation est dans un statut convertible (`potted`, `ready-to-pot`, `growing` avec racines établies).  
   - S'assurer que `child_plant_id` est `None` ou que l'utilisateur confirme un remplacement.
2. **Formulaire/flux**
   - Charger la propagation (`GET /api/propagations/{id}`) et les champs du parent (`GET /api/plants/{parent_plant_id}`) pour calculer les valeurs héritées.
   - Afficher : dates, statistiques, dernier événement, mesures, notes. Ajouter bouton `Convert to plant` accompagné d'un champ `Nom` (prérempli) et d'un sélecteur `Lieu`.
   - Option `inherit_parent_settings` (coché par défaut) qui copie les IDs de fréquence, méthode, lumière, etc.
3. **Conversion**
   - Si l'utilisateur souhaite créer une nouvelle plante, on envoie `POST /api/plants` avec les champs hérités + le nom-proposé.  
   - Une fois le `plant_id` obtenu, appeler `POST /api/propagations/{id}/convert` avec `child_plant_id` = nouvel ID et `success_date` (optionnelle, par défaut `date.today()`).  
   - Mettre à jour l'interface (naviguer vers la plante fille ou afficher la nouvelle relation mère/fille).  
4. **Suivi**
   - Créer un premier `PlantHistory` ou `PropagationEvent` lié à la nouvelle plante avec la dernière mesure de la propagation pour maintenir la continuité.  
   - Exposer les liens `parent_plant` / `child_plant` dans l'arbre généalogique et les statistiques (`PropagationAnalyticsService`).

## 5. Prochaines étapes avant codage

- [ ] Définir la structure exacte du formulaire (champs requis, validations) et préparer les composants React (`PropagationDetails`, `PropagationCard`).
- [ ] Implémenter le support backend pour créer la plante (si nécessaire) et commander la double opération `POST /api/plants` + `POST /api/propagations/{id}/convert` dans un nouveau service `PropagationConversionService`.
- [ ] Ajouter la documentation du bouton `Convert to plant` (texte d'aide et liens vers le plan) dans les docs utilisateur/idéalement dans `docs/QUICKSTART_PROPAGATION.md`.

Ce plan permet de sécuriser la conversion et de savoir exactement quelles données sont conservées pendant le passage de la bouture à la plante établie.