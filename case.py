from pip import main
from constantes import *


    
"""----------------------------------------CASE------------------------------------------"""
class Case :
    def __init__(self, colonne=-1, ligne=-1) -> None:
        

        # CONSTRUCTEUR SOUS FORME LETTRE-CHIFFRE
        if not isinstance(colonne, int) :
            if ligne != 'X' and ((ligne < 1) or (ligne > 8)):
                raise ValueError("ligne doit être entre 1 et 8 : " + str(ligne))
            if colonne != 'X' and (colonne < 'A' or colonne > 'H') :
                raise ValueError("colonne doit être entre 'A' et 'H' : " + colonne)
            
            #ATTRIBUTS
            self.colonne = totColNorm(colonne)
            self.ligne = toLigNorm(ligne)
        
        # CONSTRUCTEUR NORMALISE     
        else :
            if not coordValidesConstructeur(colonne, ligne) :
                raise ValueError("ligne et colonne doivent être entre -1 et 7 : " + str(colonne) + "," + str(ligne))
            
            #ATTRIBUTS
            self.colonne = colonne
            self.ligne = ligne
        
    def __str__(self) -> str:
        return toNNCol(self.colonne) + str(toNNLine(self.ligne))

    def __repr__(self) -> str:
        return toNNCol(self.colonne) + str(toNNLine(self.ligne))

    def equalsTo(self, case) :
        verifieTypeCase(case)
        if self.colonne != case.colonne :
            return False
        if self.ligne != case.ligne :
            return False
        return True
"""----------------------------------------FIN CASE--------------------------------------"""

"""------------------FONCTIONS UTILES-------------------"""
def verifieTypeCase(case):
    if not isinstance(case, Case):
        raise ValueError("case doit être de type Case")

def coordValides(lig, col):
    if lig >= 0 and col >= 0 and lig <=7 and col <= 7:
        return True
    return False

def coordValidesConstructeur(lig, col):
    if lig >= -1 and col >= -1 and lig <=7 and col <= 7:
        return True
    return False

# Renvoie valeur non normalisée de ligne (entre 1 et 8)
def toNNLine(ligNorm):
    return ligNorm + 1

# Renvoie valeur non normalisée de colonne (entre A et H)
def toNNCol(colNorm):
    return chr(ord('A') + colNorm)

# Renvoie valeur normalisée (entre 0 et 7) de la ligne 
def toLigNorm(lig) :
    return lig - 1

# Renvoie valeur normalisée (entre 0 et 7) de la colonne
def totColNorm(col) :
    return ord(col) - ord('A')

"""------------------------------------------------------"""