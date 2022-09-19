from case import *

"""---------------------------------------PIECE----------------------------------------"""
class Piece :
    def __init__(self, couleur, nature, case=Case()):
        if couleur != NOIR and couleur != BLANC:
            raise ValueError("couleur doit être 1 (blanc) ou 0 (noir) : " + couleur)
        if nature < ROI or nature > PION :
            raise ValueError("nature doit être entre ", ROI, " et ", PION, " : ", nature) 
        verifieTypeCase(case)

        #ATTRIBUTS
        self.couleur = couleur
        self.nature = nature 
        self.case = case
        self.enPassant = False # True si la piece peut etre mangee en passant
        self.alreadyMoved = False # True si piece a deja bouge, utilisé par roi et tours pour le roque

    def __str__(self) -> str:
        couleur = "blanc" if self.couleur == BLANC else "noir"

        if self.nature == ROI:
            nature = "Roi"
        elif self.nature == DAME:
            nature = "Dame" 
        elif self.nature == TOUR:
            nature = "Tour"
        elif self.nature == FOU:
            nature = "Fou"
        elif self.nature == CAVALIER:
            nature = "Cavalier"
        else:
            nature = "Pion"

        return nature + " " + couleur + " en " + str(self.case) 

    def equalsTo(self, piece):
        if not isinstance(piece,Piece):
            raise ValueError("L'argument @piece devrait etre de type Piece : ", type(piece))
        if self.couleur != piece.couleur:
            return False
        if not self.case.equalsTo(piece.case):
            return False
        if self.nature != piece.nature :
            return False
        return True

    def estMangee(self):
        if self.case.equalsTo(Case()): #Case() correspond à la case poubelle
            return True
        else:
            return False
"""--------------------------------------FIN PIECE---------------------------------------"""