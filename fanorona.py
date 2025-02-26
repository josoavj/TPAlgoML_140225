import pygame
from noeud import Noeud

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR_FENETRE = 300
HAUTEUR_FENETRE = 300
TAILLE_CASE = 100
COULEUR_FOND = (255, 255, 255)
COULEUR_LIGNE = (255, 255, 255)
Noir = (0, 0, 0)
Gris = (150, 150, 150)

# Création de la fenêtre
screen = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Fanorona 3x3")

# Charger l'image de fond
image_fond = pygame.image.load("assets/F1.jpg")
image_fond = pygame.transform.scale(image_fond, (LARGEUR_FENETRE, HAUTEUR_FENETRE))

# Instance de la classe Noeud pour l'état du jeu
noeud_actuel = Noeud()

# Joueur actuel
joueur_actuel = 1

# Listes pour stocker les positions des clics et les coups
clics = []
coups_p1 = 0
coups_p2 = 0

# Dictionnaire pour stocker les rectangles des boutons
boutons = {}

# Fonction pour dessiner les symboles (X ou O) sous forme de boutons
def dessiner_symboles():
    for i in range(3):
        for j in range(3):
            noeud_actuel.grille[0][0] = noeud_actuel.grille[0][1] = noeud_actuel.grille[0][2] = 1
            noeud_actuel.grille[2][0] = noeud_actuel.grille[2][1] = noeud_actuel.grille[2][2] = -1
            if noeud_actuel.grille[i][j] == 1:
                x = j * TAILLE_CASE + TAILLE_CASE // 2
                y = i * TAILLE_CASE + TAILLE_CASE // 2
                pygame.draw.circle(screen, Noir, (x, y), TAILLE_CASE // 3)  # Taille réduite
                rect = pygame.Rect(x - TAILLE_CASE // 3, y - TAILLE_CASE // 3, TAILLE_CASE // 1.5, TAILLE_CASE // 1.5)
                boutons[(i, j)] = rect
            elif noeud_actuel.grille[i][j] == -1:
                x = j * TAILLE_CASE + TAILLE_CASE // 2
                y = i * TAILLE_CASE + TAILLE_CASE // 2
                pygame.draw.circle(screen, Gris, (x, y), TAILLE_CASE // 3)  # Taille réduite
                rect = pygame.Rect(x - TAILLE_CASE // 3, y - TAILLE_CASE // 3, TAILLE_CASE // 1.5, TAILLE_CASE // 1.5)
                boutons[(i, j)] = rect

# Fonction pour vérifier le gagnant
def verifier_gagnant():
    return noeud_actuel.check_winner()

# Fonction pour vérifier si la grille est pleine
def verifier_grille_pleine():
    return noeud_actuel.est_pleine()

# Boucle principale du jeu
running = True
mouvements = []
case_origine = None


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            i, j = y // TAILLE_CASE, x // TAILLE_CASE

            if noeud_actuel.grille[i][j] == joueur_actuel:
                case_origine = (i, j)
                mouvements = noeud_actuel.deplacements_possibles(i, j)

        elif event.type == pygame.MOUSEBUTTONUP:
            if case_origine is not None:
                x, y = pygame.mouse.get_pos()
                i, j = y // TAILLE_CASE, x // TAILLE_CASE

                if (i, j) in mouvements:
                    noeud_actuel.grille[i][j] = joueur_actuel
                    noeud_actuel.grille[case_origine[0]][case_origine[1]] = 0

                    joueur_actuel = -joueur_actuel
                    case_origine = None
                    mouvements = []

    # Afficher l'image de fond
    screen.blit(image_fond, (0, 0))

    # Dessiner les symboles sous forme de boutons
    dessiner_symboles()

    # Vérifier le gagnant
    if coups_p1 == 3 and coups_p2 == 3:
        gagnant = verifier_gagnant()
        if gagnant:
            print(f"Le gagnant est : {gagnant}")
        elif verifier_grille_pleine():
            print("Match nul !")

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
