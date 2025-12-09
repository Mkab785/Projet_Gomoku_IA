# ♟️ Moteur d'Intelligence Artificielle pour le Gomoku

Ce projet est l'implémentation complète du jeu de **Gomoku** (Cinq d'affilée) en Python, intégrant un puissant moteur d'Intelligence Artificielle (IA) capable de jouer contre un humain sur un plateau 15x15.

## 🎯 Caractéristiques Clés du Moteur IA ("Thanos")

Le moteur IA, surnommé **"Thanos"** dans le code, utilise des algorithmes classiques et des techniques d'optimisation avancées pour prendre des décisions stratégiques et efficaces.

---

### 1. Algorithme Minimax avec Élagage Alpha-Bêta (Alpha-Beta Pruning)

* **Recherche Profonde :** L'IA explore l'arbre des coups possibles jusqu'à une **profondeur de recherche fixe (5)**.
* **Optimisation Cruciale :** L'utilisation de l'élagage **Alpha-Beta** (`alpha` et `beta` dans la fonction `minimax`) permet de tailler les branches de l'arbre qui ne mèneront pas au meilleur résultat, assurant une **meilleure performance** et une prise de décision rapide. 

### 2. Fonction d'Évaluation Heuristique Sophistiquée

La fonction `evaluer_plateau` est le cœur stratégique du moteur. Elle attribue un score à un état donné du jeu en analysant méticuleusement la valeur de chaque alignement pour le joueur et pour l'adversaire :

| Alignement (pions) | Niveau d'Ouverture | Score | Objectif |
| :--- | :--- | :--- | :--- |
| $\ge 5$ | N/A | $\pm \infty$ | Victoire ou Défaite immédiate |
| 4 | **2 extrémités libres** | 10 000 | Menace critique / Coup gagnant imminent |
| 3 | **2 extrémités libres** | 2 000 | Forte menace |
| 2 | **2 extrémités libres** | 200 | Préparation d'alignement |

### 3. Techniques d'Optimisation de la Recherche

* **Zone Englobante (`zone_englobante`) :** Pour ne pas évaluer inutilement les cases vides éloignées, l'IA se concentre uniquement sur les coups possibles situés dans une **zone restreinte (`marge=2`)** autour des pions déjà joués.
* **Tri et Limitation des Coups (`moves_eval`) :** Les coups possibles sont triés par score heuristique rapide. Seuls les **10 meilleurs coups** sont ensuite explorés en profondeur par l'algorithme Minimax, ce qui maximise l'efficacité de l'élagage Alpha-Beta.

### 4. Stratégie de Jeu et Règles Spécifiques

* **Stratégie de Déblocage :** L'IA priorise de manière séquentielle le **coup gagnant** puis le **coup bloquant** avant de lancer la recherche Minimax, garantissant une réponse optimale aux menaces immédiates.
* **Règle d'Ouverture (Carré 7x7) :** Le code intègre une règle d'ouverture spécifique pour le joueur Noir (`X`) lors de son deuxième coup, le forçant à jouer en dehors du carré central 7x7.

---

## 🎮 Fonctionnalités du Jeu

* **Interface Console :** Affichage simple et clair du plateau 15x15 avec un codage couleur.
* **Transcription de Partie :** Le jeu sauvegarde la séquence complète des coups joués (ex: `H7`, `G6`, etc.) à la fin de la partie.

## 🚀 Utilisation

1.  Clonez ce dépôt.
2.  Exécutez le script Python `Gomoku_Pahlawan_Portal_HannaGerguis_Kabir.py`.
3.  Choisissez de jouer les Noirs (`X`) ou les Blancs (`O`).
4.  Entrez vos coordonnées (ex : `E5`, `K10`) lorsque c'est votre tour.
