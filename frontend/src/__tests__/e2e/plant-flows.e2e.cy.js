/**
 * Tests E2E - Flows complets de l'application
 * À exécuter avec Playwright ou Cypress
 * 
 * Couvre:
 * - Création plante avec fréquences saisonnières
 * - Édition plante
 * - Affichage modale
 * - Historiques
 * - Gallery photo
 * - Page detail /plants/{id}
 */

describe('Plant Management E2E Tests', () => {
  const BASE_URL = 'http://localhost:5173'
  const API_URL = 'http://localhost:8000'

  beforeEach(() => {
    cy.visit(BASE_URL)
  })

  describe('Create Plant with Seasonal Frequencies', () => {
    it('should create a new plant with seasonal watering frequencies', () => {
      // Aller à la page de création
      cy.visit(`${BASE_URL}/plants/create`)

      // Remplir les infos de base
      cy.get('input[name="name"]').type('Test Plant Seasonal')
      cy.get('input[name="scientific_name"]').type('Test scientificus')
      cy.get('input[name="family"]').type('Araceae')

      // Remplir les infos environnement
      cy.get('input[name="temperature_min"]').type('15')
      cy.get('input[name="temperature_max"]').type('25')
      cy.get('input[name="humidity_level"]').type('60')

      // Sélectionner fréquences saisonnières
      // Printemps
      cy.get('select[name="watering_spring"]').select('2') // Régulier
      cy.get('select[name="fertilizer_spring"]').select('2') // Régulier

      // Été
      cy.get('select[name="watering_summer"]').select('1') // Fréquent
      cy.get('select[name="fertilizer_summer"]').select('1') // Fréquent

      // Automne
      cy.get('select[name="watering_fall"]').select('3') // Normal
      cy.get('select[name="fertilizer_fall"]').select('3') // Normal

      // Hiver
      cy.get('select[name="watering_winter"]').select('3') // Normal
      cy.get('select[name="fertilizer_winter"]').select('2') // Régulier

      // Soumettre
      cy.get('button[type="submit"]').click()

      // Vérifier la redirection et affichage
      cy.url().should('include', '/plants')
      cy.contains('Test Plant Seasonal').should('be.visible')
    })

    it('should display seasonal frequencies in modal', () => {
      // Ouvrir une plante existante
      cy.get('[data-testid="plant-card"]').first().click()

      // Vérifier la modale
      cy.get('[data-testid="modal-container"]').should('be.visible')

      // Vérifier que les fréquences saisonnières s'affichent
      cy.contains('Arrosage par saison').should('be.visible')
      cy.contains('Fertilisation par saison').should('be.visible')

      // Vérifier les cartes de saison
      cy.contains('Saison actuelle').should('be.visible')
      cy.contains('Saison future').should('be.visible')

      // Vérifier que les fréquences ont une valeur (pas vide)
      cy.get('[data-testid="seasonal-watering-current"]')
        .should('contain', 'Fréquent', 'Régulier', 'Normal', 'Rare')
    })

    it('should update seasonal frequencies', () => {
      // Ouvrir une plante pour édition
      cy.get('[data-testid="plant-card"]').first().click()
      cy.get('[data-testid="modal-edit-button"]').click()

      // Changer une fréquence
      cy.get('select[name="watering_summer"]').select('3') // Changer à Normal
      cy.get('button[type="submit"]').click()

      // Vérifier la modification
      cy.visit(BASE_URL)
      cy.get('[data-testid="plant-card"]').first().click()
      cy.contains('Été').parent()
        .should('contain', 'Normal')
    })
  })

  describe('Modal Plant Detail', () => {
    it('should display all card sections', () => {
      cy.get('[data-testid="plant-card"]').first().click()

      // Vérifier la présence de toutes les cartes
      cy.contains('Besoins').should('be.visible')
      cy.contains('Arrosage par saison').should('be.visible')
      cy.contains('Fertilisation par saison').should('be.visible')
      cy.contains('Dernier arrosage').should('be.visible')
      cy.contains('Dernière fertilisation').should('be.visible')
      cy.contains('Dernier rempotage').should('be.visible')
      cy.contains('Maladie').should('be.visible')
    })

    it('should open action forms', () => {
      cy.get('[data-testid="plant-card"]').first().click()

      // Test bouton "Créer" pour arrosage
      cy.get('[data-testid="btn-create-watering"]').click()
      cy.get('[data-testid="watering-form"]').should('be.visible')
      cy.get('[data-testid="form-close"]').click()

      // Test bouton "Créer" pour fertilisation
      cy.get('[data-testid="btn-create-fertilizing"]').click()
      cy.get('[data-testid="fertilizing-form"]').should('be.visible')
      cy.get('[data-testid="form-close"]').click()

      // Test bouton "Créer" pour rempotage
      cy.get('[data-testid="btn-create-repotting"]').click()
      cy.get('[data-testid="repotting-form"]').should('be.visible')
      cy.get('[data-testid="form-close"]').click()

      // Test bouton "Créer" pour maladie
      cy.get('[data-testid="btn-create-disease"]').click()
      cy.get('[data-testid="disease-form"]').should('be.visible')
    })

    it('should handle photo carousel correctly', () => {
      cy.get('[data-testid="plant-card"]').first().click()

      // Ouvrir carousel
      cy.get('[data-testid="photo-main"]').click()
      cy.get('[data-testid="carousel"]').should('be.visible')

      // Naviguer
      cy.get('[data-testid="carousel-next"]').click()
      cy.get('[data-testid="carousel-prev"]').click()

      // Fermer carousel sans fermer modale
      cy.get('[data-testid="carousel-close"]').click()
      cy.get('[data-testid="carousel"]').should('not.exist')
      cy.get('[data-testid="modal-container"]').should('be.visible')
    })

    it('should display gallery thumbnails', () => {
      cy.get('[data-testid="plant-card"]').first().click()

      // Vérifier la présence de la galerie
      cy.contains('Galerie').should('be.visible')
      cy.get('[data-testid="gallery-thumb"]').should('have.length.at.least', 1)

      // Cliquer sur une thumbnail
      cy.get('[data-testid="gallery-thumb"]').first().click()
      // Vérifier que la modale reste ouverte
      cy.get('[data-testid="modal-container"]').should('be.visible')
    })
  })

  describe('Plant Detail Page (/plants/{id})', () => {
    it('should display exact same content as modal', () => {
      // Récupérer l'ID de la première plante
      cy.get('[data-testid="plant-card"]')
        .first()
        .invoke('attr', 'data-plant-id')
        .then(plantId => {
          cy.visit(`${BASE_URL}/plants/${plantId}`)

          // Vérifier que c'est la même structure que la modale
          cy.get('[data-testid="modal-container"]').should('be.visible')
          cy.contains('Besoins').should('be.visible')
          cy.contains('Arrosage par saison').should('be.visible')
          cy.contains('Fertilisation par saison').should('be.visible')
        })
    })

    it('should be able to edit from detail page', () => {
      cy.get('[data-testid="plant-card"]')
        .first()
        .invoke('attr', 'data-plant-id')
        .then(plantId => {
          cy.visit(`${BASE_URL}/plants/${plantId}`)
          cy.get('[data-testid="edit-button"]').click()
          cy.url().should('include', 'edit')
        })
    })
  })

  describe('Home Page / Plant List', () => {
    it('should display plant cards', () => {
      cy.get('[data-testid="plant-card"]').should('have.length.greaterThan', 0)
    })

    it('should filter/search plants', () => {
      // Si un search existe
      cy.get('[data-testid="search-input"]').type('Monstera')
      cy.get('[data-testid="plant-card"]')
        .should('have.length.at.least', 1)
    })

    it('should open plant detail from card', () => {
      cy.get('[data-testid="plant-card"]').first().click()
      cy.get('[data-testid="modal-container"]').should('be.visible')
    })
  })

  describe('Mobile Responsiveness', () => {
    beforeEach(() => {
      // Set mobile viewport
      cy.viewport('iphone-x')
    })

    it('should adapt modal layout for mobile', () => {
      cy.get('[data-testid="plant-card"]').first().click()

      // Vérifier que les colonnes se stackent
      cy.get('[data-testid="modal-left-column"]')
        .should('have.css', 'width')

      // Vérifier que les 4 cartes historiques s'affichent correctement
      cy.get('[data-testid="history-card"]').should('be.visible')
    })

    it('should make forms mobile-friendly', () => {
      cy.visit(`${BASE_URL}/plants/create`)

      // Vérifier que les inputs sont cliquables
      cy.get('input[name="name"]').should('be.visible').click().type('Test')
      cy.get('select[name="watering_spring"]').should('be.visible')
    })

    it('should display buttons correctly on mobile', () => {
      cy.get('[data-testid="plant-card"]').first().click()

      // Boutons d'action
      cy.get('[data-testid="btn-create-watering"]').should('be.visible')
      cy.get('[data-testid="btn-create-fertilizing"]').should('be.visible')
    })
  })

  describe('Complete Workflow', () => {
    it('should complete full user journey', () => {
      // 1. Aller à l'accueil
      cy.url().should('include', '/plants')

      // 2. Créer une nouvelle plante
      cy.get('[data-testid="create-button"]').click()
      cy.url().should('include', '/create')

      // 3. Remplir le formulaire (simplifié)
      cy.get('input[name="name"]').type('Complete Test Plant')
      cy.get('input[name="family"]').type('Araceae')
      cy.get('button[type="submit"]').click()

      // 4. Ouvrir la modale de la nouvelle plante
      cy.contains('Complete Test Plant').click()
      cy.get('[data-testid="modal-container"]').should('be.visible')

      // 5. Créer un arrosage
      cy.get('[data-testid="btn-create-watering"]').click()
      cy.get('[data-testid="watering-form"]').should('be.visible')
      cy.get('input[type="date"]').type('2025-11-02')
      cy.get('button[type="submit"]').click()

      // 6. Vérifier que l'historique s'est mis à jour
      cy.contains('Dernier arrosage').parent()
        .should('contain', '2 novembre 2025')

      // 7. Retour à l'accueil
      cy.get('[data-testid="back-button"]').click()
      cy.url().should('include', '/plants')
    })
  })
})
