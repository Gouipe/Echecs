Jeu d'échecs en local codé en python avec la librairie pygame. Les joueurs doivent cliquer sur la pièce à bouger,
puis sur une case d'arrivée valide (les blancs commencent).

Les règles suivantes sont implémentées:
-EN PASSANT décrite sur wikipedia comme : "la prise en passant est une possibilité particulière de capturer un pion. Lorsqu'un pion se trouve sur la 
cinquième rangée et que l'adversaire avance de deux cases un pion d'une colonne voisine (les deux pions se retrouvent 
alors côte-à-côte sur la même rangée), le premier pion peut prendre le second."
-ROQUE. Petit et grand roques sont possibles si le roi n'est attaqué ni sur la case d'origine, ni
sur la case d'arrivée après roque.
-Un pion passé (arrivé sur la dernière ligne en face de lui) se transforme en une nouvelle pièce selon le choix du joueur.