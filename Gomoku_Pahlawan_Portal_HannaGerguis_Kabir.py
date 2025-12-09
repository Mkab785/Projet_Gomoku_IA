
import random

def creation_plateau():
    # On cree un plateau 15x15 rempli de '.'
    plateau = []
    for _ in range(15):
        ligne = []
        for _ in range(15):
            ligne.append('.')
        plateau.append(ligne)
    return plateau

def affichage_plateau(plateau):
    couleur_defaut = "\033[0m"   
    couleur_rouge = "\033[31m"   
    couleur_bleue = "\033[34m"   

    en_tete = "     "
    for i in range(15):
        if i % 2 == 0 and i < 10:
            en_tete += f" {couleur_bleue}{i}   {couleur_defaut}"
        elif i % 2 == 0 and i >= 10:
            en_tete += f"{couleur_bleue}{i}   {couleur_defaut}"
        elif i < 10:
            en_tete += f" {couleur_rouge}{i}   {couleur_defaut}"
        else:
            en_tete += f"{couleur_rouge}{i}   {couleur_defaut}"
    print(en_tete.rstrip())

    print("   +" + "----+" * 15)
    for idx, row in enumerate(plateau):
        ligne = f"{chr(65 + idx)}  |"
        for col_idx, cell in enumerate(row):
            if col_idx % 2 == 0:
                ligne += f"  {couleur_bleue}{cell}{couleur_defaut} |"
            else:
                ligne += f"  {couleur_rouge}{cell}{couleur_defaut} |"
        print(ligne)
        print("   +" + "----+" * 15)

def placer_pion(plateau, ligne, colonne, pion):
    if 0 <= ligne < 15 and 0 <= colonne < 15:
        if plateau[ligne][colonne] == '.':
            plateau[ligne][colonne] = pion
            return True
        else:
            print("Erreur : La case est déjà occupée.")
            return False
    else:
        print("Erreur : Position en dehors du plateau.")
        return False

def compter_pions(plateau, pion):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    max_alignes = {'horizontal': 0, 'vertical': 0, 'diag_desc': 0, 'diag_mont': 0}
    for ligne in range(15):
        for colonne in range(15):
            if plateau[ligne][colonne] == pion:
                for idx, (delta_ligne, delta_colonne) in enumerate(directions):
                    count = 1
                    x, y = ligne + delta_ligne, colonne + delta_colonne
                    while 0 <= x < 15 and 0 <= y < 15 and plateau[x][y] == pion:
                        count += 1
                        x += delta_ligne
                        y += delta_colonne
                    keys = ['horizontal', 'vertical', 'diag_desc', 'diag_mont']
                    max_alignes[keys[idx]] = max(max_alignes[keys[idx]], count)
    return max_alignes

def est_gagne(plateau, pion):
    max_alignes = compter_pions(plateau, pion)   # verif si pion a au moins 5 pions alignés
    return (max(max_alignes.values()) >= 5)

# --------------------------------------------------------------------
# Fonctions d'évaluation
# --------------------------------------------------------------------

def evaluer_aligne(plateau, lig, col, dlig, dcol, joueur):
    nb = 0
    tmp_lig, tmp_col = lig, col

    while 0 <= tmp_lig < 15 and 0 <= tmp_col < 15 and plateau[tmp_lig][tmp_col] == joueur:
        nb += 1
        tmp_lig += dlig
        tmp_col += dcol

    avant_libre = (0 <= tmp_lig < 15 and 0 <= tmp_col < 15 and plateau[tmp_lig][tmp_col] == '.')

    tmp_lig2, tmp_col2 = lig - dlig, col - dcol
    nb_arriere = 0
    while 0 <= tmp_lig2 < 15 and 0 <= tmp_col2 < 15 and plateau[tmp_lig2][tmp_col2] == joueur:
        nb_arriere += 1
        tmp_lig2 -= dlig
        tmp_col2 -= dcol

    arriere_libre = (0 <= tmp_lig2 < 15 and 0 <= tmp_col2 < 15 and plateau[tmp_lig2][tmp_col2] == '.')

    nb_total = nb + nb_arriere
    ext_ouvertes = 0
    if avant_libre:
        ext_ouvertes += 1
    if arriere_libre:
        ext_ouvertes += 1

    return nb_total, ext_ouvertes

def score_local(aligne, sans_bornes):
    if aligne >= 5:
        return float('inf')
    if aligne == 4:
        if sans_bornes == 2:
            return 10000
        elif sans_bornes == 1:
            return 500
        else:
            return 50
    elif aligne == 3:
        if sans_bornes == 2:
            return 2000
        elif sans_bornes == 1:
            return 200
        else:
            return 20
    elif aligne == 2:
        if sans_bornes == 2:
            return 200
        elif sans_bornes == 1:
            return 20
        else:
            return 2
    elif aligne == 1:
        return 1
    return 0

def evaluer_plateau(plateau, pion):
    ennemi = 'X' if pion == 'O' else 'O'
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    points = 0

    for lig in range(15):
        for col in range(15):
            if plateau[lig][col] == pion:
                for dlig, dcol in dirs:
                    nb_total, ext_ouvertes = evaluer_aligne(plateau, lig, col, dlig, dcol, pion)
                    valeur = score_local(nb_total, ext_ouvertes)
                    if valeur == float('inf'):
                        return float('inf')
                    points += valeur
            elif plateau[lig][col] == ennemi:
                for dlig, dcol in dirs:
                    nb_total, ext_ouvertes = evaluer_aligne(plateau, lig, col, dlig, dcol, ennemi)
                    valeur = score_local(nb_total, ext_ouvertes)
                    if valeur == float('inf'):
                        return -float('inf')
                    points -= valeur
    return points

# --------------------------------------------------------------------
# Coup gagnant, menaces, etc
# --------------------------------------------------------------------

def trouver_coup_gagnant(plateau, pion):
    for i in range(15):
        for j in range(15):
            if plateau[i][j] == '.':
                # simulation
                plateau[i][j] = pion
                if est_gagne(plateau, pion):
                    plateau[i][j] = '.'
                    return (i, j)
                plateau[i][j] = '.'
    return None

def analyser_menaces_globales(plateau, pion):
    adversaire = 'X' if pion == 'O' else 'O'
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    menaces = []
    for ligne in range(15):
        for colonne in range(15):
            if plateau[ligne][colonne] == adversaire:
                count = 1
                for delta_ligne, delta_colonne in directions:
                    x, y = ligne + delta_ligne, colonne + delta_colonne
                    espaces_vides = []
                    count = 1
                    while 0 <= x < 15 and 0 <= y < 15:
                        if plateau[x][y] == adversaire:
                            count += 1
                        elif plateau[x][y] == '.':
                            espaces_vides.append((x, y))
                        else:
                            break
                        x += delta_ligne
                        y += delta_colonne
                    if count >= 3 and len(espaces_vides) > 0:
                        for case_vide in espaces_vides:
                            menaces.append(case_vide)
    return menaces

# --------------------------------------------------------------------
# zone englobante et coups possibles
# --------------------------------------------------------------------
def zone_englobante(plateau, marge=2):
    lig_min, lig_max = 14, 0
    col_min, col_max = 14, 0
    trouve_pion = False

    for lig in range(15):
        for col in range(15):
            if plateau[lig][col] != '.':
                trouve_pion = True
                if lig < lig_min:
                    lig_min = lig
                if lig > lig_max:
                    lig_max = lig
                if col < col_min:
                    col_min = col
                if col > col_max:
                    col_max = col
    if not trouve_pion:
        return 0, 14, 0, 14

    lig_min = max(0, lig_min - marge)
    lig_max = min(14, lig_max + marge)
    col_min = max(0, col_min - marge)
    col_max = min(14, col_max + marge)
    return lig_min, lig_max, col_min, col_max

def obtenir_coups_possibles(plateau, marge=2):  
    coups = []
    min_x, max_x, min_y, max_y = zone_englobante(plateau, marge)
    for i in range(min_x, max_x+1):
        for j in range(min_y, max_y+1):
            if plateau[i][j] == '.':
                coups.append((i, j))
    return coups

def obtenir_toutes_les_cases_vides(plateau):
    coups = []
    for i in range(15):
        for j in range(15):
            if plateau[i][j] == '.':
                coups.append((i, j))
    return coups

# --------------------------------------------------------------------
# Minimax optimisé 
# --------------------------------------------------------------------
def minimax(plateau, profondeur, alpha, beta, maximiser, pion, liste_coups):
    adversaire = 'X' if pion == 'O' else 'O'

    # Condition d arret
    if profondeur == 0 or est_gagne(plateau, pion) or est_gagne(plateau, adversaire):
        return evaluer_plateau(plateau, pion), None

    if not liste_coups:
        # aucun coup possible
        if maximiser:
            return (-9999, None)
        else:
            return (9999, None)


    moves_eval = []
    for (x, y) in liste_coups:
        if maximiser:
            plateau[x][y] = pion
            val = evaluer_plateau(plateau, pion)
            plateau[x][y] = '.'
        else:
            plateau[x][y] = adversaire
            val = evaluer_plateau(plateau, pion)
            plateau[x][y] = '.'
        moves_eval.append(((x, y), val))

    # Tri en fonction du score rapide
    if maximiser:
        moves_eval.sort(key=lambda x: x[1], reverse=True)
    else:
        moves_eval.sort(key=lambda x: x[1])
    moves_eval = moves_eval[:10]

    meilleur_coup = None

    if maximiser:
        meilleur_score = float('-inf')
        for (coup, _) in moves_eval:
            x, y = coup
            plateau[x][y] = pion
            new_coups = obtenir_coups_possibles(plateau)
            score, _ = minimax(plateau, profondeur-1, alpha, beta, False, pion, new_coups)
            plateau[x][y] = '.'

            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = (x, y)

            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return (meilleur_score, meilleur_coup)

    else:
        meilleur_score = float('inf')
        for (coup, _) in moves_eval:
            x, y = coup
            plateau[x][y] = adversaire
            new_coups = obtenir_coups_possibles(plateau)
            score, _ = minimax(plateau, profondeur-1, alpha, beta, True, pion, new_coups)
            plateau[x][y] = '.'

            if score < meilleur_score:
                meilleur_score = score
                meilleur_coup = (x, y)

            beta = min(beta, score)
            if beta <= alpha:
                break
        return (meilleur_score, meilleur_coup)

def ia_jouer(plateau, pion, profondeur=5, restriction_carre=False):
    adversaire = 'X' if pion == 'O' else 'O'

    # 1) coup gagnant ?
    coup_gagnant = trouver_coup_gagnant(plateau, pion)
    if coup_gagnant:
        print(f"Thanos ({pion}) joue pour gagner : {chr(coup_gagnant[0]+65)}{coup_gagnant[1]}")
        return coup_gagnant

    # 2) coup bloquant ?
    coup_bloquant = trouver_coup_gagnant(plateau, adversaire)
    if coup_bloquant:
        print(f"Thanos ({pion}) bloque un coup gagnant adverse : {chr(coup_bloquant[0]+65)}{coup_bloquant[1]}")
        return coup_bloquant

    # 3) Préparation des coups possibles
    if restriction_carre and pion == 'X':
        all_free = obtenir_toutes_les_cases_vides(plateau)
        
        coups_possibles = [(x, y) for (x, y) in all_free 
                           if (x == 3 or x == 11 or y == 3 or y == 11)]
        
        if not coups_possibles:
            coups_possibles = all_free  

        score, meilleur_coup = minimax(
            plateau, profondeur, float('-inf'), float('inf'), True,
            pion, coups_possibles
        )
    else:
        coups_possibles = obtenir_coups_possibles(plateau)
        score, meilleur_coup = minimax(
            plateau, profondeur, float('-inf'), float('inf'), True,
            pion, coups_possibles
        )

    # 4) Si on a trouvé un coup via Minimax
    if meilleur_coup:
        print(f"Thanos ({pion}) joue via Minimax : {chr(meilleur_coup[0]+65)}{meilleur_coup[1]}")
        return meilleur_coup

    # 5) Sinon coup aléatoire
    print(f"Thanos ({pion}) n'a pas trouvé de coup Minimax, coup aléatoire.")
    if not coups_possibles:
        coups_possibles = obtenir_toutes_les_cases_vides(plateau)
        if not coups_possibles:
            print("Aucun coup possible.")
            return None
    return random.choice(coups_possibles)

# --------------------------------------------------------------------
# Fonctions de jeu
# --------------------------------------------------------------------

def jouer_humain_vs_ia():
    plateau = creation_plateau()

    reponse = input("Voulez-vous jouer X (Noir) ou O (Blanc)? [X/O]: ").strip().upper()
    if reponse not in ['X','O']:
        reponse = 'X' 
        print("Aucune réponse valable, vous serez 'X'")

    if reponse == 'X':
        joueurs = [('X', 'humain'), ('O', 'Thanos')]
    else:
        joueurs = [('X', 'Thanos'), ('O', 'humain')]

    pion_noir, type_joueur_noir = joueurs[0]
    pion_blanc, type_joueur_blanc = joueurs[1]

    placer_pion(plateau, 7, 7, pion_noir)
    affichage_plateau(plateau)

    nb_coups_noir = 1  
    transcription = ["H7"]
    partie_en_cours = True
    tour = 1

    while partie_en_cours: #lancement de la partie 
        index_joueur = tour % 2
        pion_actuel, type_joueur = joueurs[index_joueur]
        if pion_actuel == 'X' and nb_coups_noir == 1:
            restriction = True
        else:
            restriction = False

        # tour de l'humain ou l'ia 
        if type_joueur == 'humain':
            print(f"\nÀ vous de jouer, vous êtes '{pion_actuel}'.")
            coup_valide = False
            while not coup_valide:
                entree = input("Coordonnées (ex: H7, D0...)? ").strip().upper()
                if len(entree) < 2:
                    print("Entrée invalide. Réessayez.")
                    continue

                ligne = ord(entree[0]) - 65
                col_str = entree[1:].strip() 
                colonne = int(col_str) if col_str.isdigit() else -1
                if restriction and pion_actuel == 'X':
                    if 3 < ligne < 11 and 3 < colonne < 11:
                        print("Erreur : pas dans le carré 7x7 pour le 2e coup de Noir.")
                        continue

                if 0 <= ligne < 15 and 0 <= colonne < 15:
                    if placer_pion(plateau, ligne, colonne, pion_actuel):
                        transcription.append(f"{chr(65 + ligne)}{colonne}")
                        affichage_plateau(plateau)
                        coup_valide = True
                        if est_gagne(plateau, pion_actuel):
                            print(f"\nFélicitations ! Le joueur '{pion_actuel}' a gagné !")
                            print(f"Transcription des coups : {transcription}")
                            partie_en_cours = False
                        else:
                            if pion_actuel == 'X':
                                nb_coups_noir += 1         
                    else:
                        print("La case est déjà occupée. Réessayez.")
                else:
                    print("Coordonnées invalides. Réessayez.")

        else:
            print(f"\nC'est au tour de Thanos ({pion_actuel}).")
            lg, col = ia_jouer(plateau, pion_actuel, restriction_carre=restriction)
            placer_pion(plateau, lg, col, pion_actuel)
            transcription.append(f"{chr(65 + lg)}{col}")
            affichage_plateau(plateau)

            # verif de victoire
            if est_gagne(plateau, pion_actuel):
                print(f"\nThanos ({pion_actuel}) a gagné !")
                print(f"Transcription des coups : {transcription}")
                partie_en_cours = False
            else:
                if pion_actuel == 'X':
                    nb_coups_noir += 1

        # verif si plateau plein (match nul)
        if '.' not in [cell for row in plateau for cell in row]:
            print("\nMatch nul, plateau plein.")
            print(f"Transcription des coups : {transcription}")
            partie_en_cours = False

        # si c'est pas fini on continue
        if partie_en_cours:
            tour += 1

jouer_humain_vs_ia()
