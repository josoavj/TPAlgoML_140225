# creation du noeud: état intial du plateau

class Noeud:
    def __init__(self, grille=None, joueur_actuel=1, parent=None):

        if grille is None:
            # Position des pions selon l'image fournie
            self.grille = [
                [1, 1, 1],  # Joueur 1 (O) en haut aux coins
                [0, 0, 0],  # Ligne vide au centre
                [-1, -1, -1]  # Joueur 2 (X) en bas aux coins
            ]
        else:
            self.grille = [ligne[:] for ligne in grille]  # Copie du plateau

        self.joueur_actuel = joueur_actuel
        self.parent = parent
        self.enfants = []

    def afficher_grille(self):
        """Affiche le plateau sous forme lisible."""
        symbols = {0: ".", 1: "X", -1: "O"}
        for ligne in self.grille:
            print(" ".join(symbols[cell] for cell in ligne))

    def deplacements_possibles(self, x, y):
        """Retourne une liste des mouvements valides pour un pion donné."""
        directions = [
            (0, 1),  # Déplacement horizontal à droite
            (0, -1),  # Déplacement horizontal à gauche
            (1, 0),  # Déplacement vertical vers le bas
            (-1, 0),  # Déplacement vertical vers le haut
        ]

        # Liste des coins où les pions peuvent se déplacer en diagonale
        croix_intersections = [(0, 0), (0, 2), (2, 0), (2, 2)]  # Coins de la grille
        mouvements = []

        # Ajout des diagonales seulement pour les coins
        if (x, y) in croix_intersections:
            directions += [
                (1, 1),  # Diagonale bas-gauche à haut-droit
                (1, -1),  # Diagonale haut-droit à bas-gauche
                (-1, 1),  # Diagonale bas-droit à haut-gauche
                (-1, -1),  # Diagonale haut-gauche à bas-droit
            ]

        # Vérification des déplacements
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Vérifier que la nouvelle position est dans la grille et vide
            if 0 <= nx < 3 and 0 <= ny < 3 and self.grille[nx][ny] == 0:
                mouvements.append((nx, ny))

        return mouvements

    # question 1: methode get_successor()
    def get_successor(self):
        """Génère tous les états possibles après un coup."""
        successors = []
        for i in range(3):
            for j in range(3):
                if self.grille[i][j] == self.joueur_actuel:  # Si c'est un pion du joueur actuel
                    for nx, ny in self.deplacements_possibles(i, j):
                        nouvelle_grille = [ligne[:] for ligne in self.grille]
                        nouvelle_grille[i][j] = 0  # Enlever le pion de sa position actuelle
                        nouvelle_grille[nx][ny] = self.joueur_actuel  # Placer à la nouvelle position
                        successors.append(Noeud(nouvelle_grille, -self.joueur_actuel, self))
        self.successors = successors
        return successors

    # question 2: methode check_winner()
    def check_winner(self):
        """Vérifie si le joueur actuel a gagné."""
        for i in range(3):
            # Vérification horizontale et verticale
            if abs(sum(self.grille[i])) == 3 or abs(sum(row[i] for row in self.grille)) == 3:
                return True
        # Vérification diagonale
        if abs(self.grille[0][0] + self.grille[1][1] + self.grille[2][2]) == 3:
            return True
        if abs(self.grille[0][2] + self.grille[1][1] + self.grille[2][0]) == 3:
            return True
        return False

    def eval(self, us):
        """Évalue l'état actuel du jeu pour le joueur 'us'."""
        if self.check_winner():
            # Si le joueur actuel a gagné, renvoie une valeur positive ou négative selon le joueur
            return 1 if self.joueur_actuel == us else -1
        # Si c'est un match nul, renvoie 0
        elif all(self.grille[i][j] != 0 for i in range(3) for j in range(3)):
            return 0  # Match nul
        return 0  # Jeu en cours (nous retournons une évaluation neutre)


# question 3: implémentation de mimimax()
def minimax(node, depth, us='X'):
    if depth == 0 or node.check_winner():
        return (node.eval(us), None)

    if node.joueur_actuel == us:
        maxEval = -1000
        best_move = None
        for child in node.get_successor():
            eval, _ = minimax(child, depth - 1, us)
            if eval > maxEval:
                maxEval = eval
                best_move = child
        return (maxEval, best_move)
    else:
        minEval = 1000
        best_move = None
        for child in node.get_successor():
            eval, _ = minimax(child, depth - 1, us)
            if eval < minEval:
                minEval = eval
                best_move = child
        return (minEval, best_move)


# question 4: implémentation d'alphabeta()
def alphabeta(node, depth, alpha, beta, us='X'):
    if depth == 0 or node.is_terminal():
        return (node.eval(us), None)
    if node.joueur_actuel == us:
        maxEval = -1000
        best_move = None
        for child in node.get_successors():
            eval, _ = alphabeta(child, depth - 1, alpha, beta, us)
            if eval > maxEval:
                maxEval = eval
                best_move = child
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return (maxEval, best_move)
    else:
        minEval = 1000
        best_move = None
        for child in node.get_successors():
            eval, _ = alphabeta(child, depth - 1, alpha, beta, us)
            if eval < minEval:
                minEval = eval
                best_move = child
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return (minEval, best_move)


# Test
noeud_initial = Noeud()

successors = noeud_initial.get_successor()
print(f"Nombre de coups possibles : {len(successors)}")
