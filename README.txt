Jeu d'échecs en local codé en python à l'aide de la librairie pygame. Je suis content de ce projet 

-------------------------------------------------------- FONCTIONNEMENT ------------------------------------------------------------------------
Il faut lancer le fichier main du projet. Apparait alors une fenêtre graphique représentant un échequier.
Les joueurs doivent cliquer sur la pièce à bouger, la pièce sélectionnée devient alors surbrillante. Il faut ensuite cliquer sur une case
d'arrivée valide. Si la case est valide la pièce déplacée, sinon il faut recommencer ces étapes. Les pièces blanches commencent.
Le jeu s'arrête lorsqu'il y a échec et mat (un roi est en échec et aucun coup ne peut le sortir de l'échec).

--------------------------------------------------------- REGLES -------------------------------------------------------------------------------
Les règles suivantes sont implémentées:

-EN PASSANT décrite sur wikipedia comme : "la prise en passant est une possibilité particulière de capturer un pion. Lorsqu'un pion se trouve 
sur la cinquième rangée et que l'adversaire avance de deux cases un pion d'une colonne voisine (les deux pions se retrouvent alors côte-à-côte 
sur la même rangée), le premier pion peut prendre le second."

-ROQUE : "Il s'agit de déplacer horizontalement le roi, sans qu'il ait encore bougé durant la partie, de deux cases vers l'une des deux tours du 
même camp et de placer la tour la plus proche du Roi, sur la case qu'il touche dans le sens contraire de son déplacement1. On parle de petit 
roque lorsque le roi et la tour (colonne h) ne sont séparés que par deux cases (sur l'aile roi), et de grand roque, lorsque les deux pièces sont
séparées par trois cases (sur l'aile dame - tour sur la colonne a)."
Pour utiliser ce coup, il faut cliquer sur le roi, puis sur la case d'arrivée du roi (donc deux cases à droite ou deux cases à gauche du roi).
Petit et grand roques ne sont possibles que si le roi n'est attaqué ni sur la case d'origine, ni sur sa case d'arrivée après roque, et que ni le 
roi ni la tour n'ont déjà été déplacés.

-Un pion passé (arrivé sur la dernière ligne) se transforme en une nouvelle pièce selon le choix du joueur.
