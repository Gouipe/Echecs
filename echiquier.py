from tkinter import E
from pip import main
from case import *
from piece import *
from constantes import *

class Echiquier :

    def __init__(self):
        self.pieces = []
        self.remplitTabPieces()

    def remplitTabPieces(self):
        for col in range(8):
            self.pieces.append(Piece(BLANC, PION, Case(chr(ord('A') + col), 2)))
        self.pieces.append(Piece(BLANC, TOUR, Case('A', 1)))
        self.pieces.append(Piece(BLANC, TOUR, Case('H', 1)))
        self.pieces.append(Piece(BLANC, CAVALIER, Case('B', 1)))
        self.pieces.append(Piece(BLANC, CAVALIER, Case('G', 1))) 
        self.pieces.append(Piece(BLANC, FOU, Case('C', 1)))
        self.pieces.append(Piece(BLANC, FOU, Case('F', 1)))
        self.pieces.append(Piece(BLANC, DAME, Case('D', 1)))
        self.pieces.append(Piece(BLANC, ROI, Case('E', 1)))

        for col in range(8):
            self.pieces.append(Piece(NOIR, PION, Case(chr(ord('A') + col), 7)))
        self.pieces.append(Piece(NOIR, TOUR, Case('A', 8)))
        self.pieces.append(Piece(NOIR, TOUR, Case('H', 8)))
        self.pieces.append(Piece(NOIR, CAVALIER, Case('B', 8)))
        self.pieces.append(Piece(NOIR, CAVALIER, Case('G', 8))) 
        self.pieces.append(Piece(NOIR, FOU, Case('C', 8)))
        self.pieces.append(Piece(NOIR, FOU, Case('F', 8)))
        self.pieces.append(Piece(NOIR, DAME, Case('D', 8)))
        self.pieces.append(Piece(NOIR, ROI, Case('E', 8)))

    #
    # Renvoie IMPOSSIBLE si aucune pièce sur @caseDepart, ou si pièce sur @caseDepart ne peut pas aller sur @caseArrivee
    # Renvoie MOVED si la pièce sur @caseDepart s'est déplacée sur @caseArrivée
    # Renvoie CHECK si le mouvement est impossible a cause d'un echec
    # Renvoie AUCUNE_PIECE si aucune piece sur caseDepart
    #
    def move(self, caseDepart, caseArrivee, couleur):
        #Vérifie si il y a une pièce sur la case de Départ
        piece = self.pieceSur(caseDepart)
        if piece == None:
            return AUCUNE_PIECE

        #Vérifie si la case d'arrivée est atteignable par la piece qui est sur la case de départ
        atteignable = False
        for case in self.movable(caseDepart):
            if case.equalsTo(caseArrivee):
                atteignable = True    
        if not atteignable:
            return IMPOSSIBLE 
    
        #Change la position de la pièce bougée (dans la liste self.pieces), et la pièce mangée le cas échéant
        pieceMangee = self.pieceSur(caseArrivee)
        if pieceMangee != None:
            self.pieceMangeeEn(caseArrivee)
        self.changePosition(caseDepart, caseArrivee)

        # La piece a bougé mais le roi de couleur @couleur est en echec, le mouvement est donc impossible
        # On annule le deplacement de pieces qui vient juste d'etre fait
        if self.echecRoi(couleur):
            # Retour de la piece qui avait bougée
            self.changePosition(caseArrivee, caseDepart)
            # Retour de la piece qui avait ete mangee le cas echeant
            if pieceMangee != None:
                pieceMangee.case = caseArrivee
            return CHECK      

        # Doit toujours etre appellee pour passer l'attribut enPassant a False si necessaire
        if self.verifieEnPassant(caseDepart, caseArrivee, pieceMangee, couleur):      
            return EN_PASSANT

        # N'est utile que si tour ou roi est bouge
        if self.verifieRoque(piece, caseArrivee):
            return ROQUE

        if self.verifiePionPasse(piece, caseArrivee):
            return PION_PASSE

        return MOVED

    #
    # Renvoie vrai si la piece et la case d'arrivée données en argument correspondent
    # à un pion arrivé au bout de l'échiquier
    #
    def verifiePionPasse(self, piece, caseArrivee):
        if piece.nature == PION and (caseArrivee.ligne == 0 or caseArrivee.ligne == 7):
            return True
        else:
            return False

    #
    # Passe l'attribut alreadyMoved a True si la piece est le roi ou une tour.
    # Si le mouvement correspondant aux arguments est un roque, le tour est bougee et
    # la fonction renvoie vrai. Renvoie faux sinon.
    #
    def verifieRoque(self, piece, caseArrivee):
        if piece.nature == ROI:
            # Cas roque effectué
            if piece.alreadyMoved == False and abs(caseArrivee.colonne - 4) == 2: # 4 correspond a la colonne d'un roi qui n'a pas bouge
                lig = caseArrivee.ligne
                # Grand roque:
                if caseArrivee.colonne == 2:
                    print("grand roque")
                    tourCaseDepart = Case(0, lig)
                    tourCaseArrivee = Case(3, lig)
                # Petit Roque
                else:
                    print("petit roque")
                    tourCaseDepart = Case(7, lig)
                    tourCaseArrivee = Case(5, lig)
                if self.pieceSur(tourCaseDepart).alreadyMoved == False:
                    print("changePosition() : " + str(self.changePosition(tourCaseDepart, tourCaseArrivee)))
                    return True
        # Cas pas de roque effectué
        piece.alreadyMoved = True
        return False


    #
    # Renvoie True si le mouvement de piece correspondant aux arguments protege de l'echec. 
    # Renvoie False sinon
    #
    def moveEchecMat(self, caseDepart, caseArrivee, couleur):
        #Change la position de la pièce bougée (dans la liste self.pieces), et la pièce mangée le cas échéant
        pieceMangee = self.pieceSur(caseArrivee)
        if pieceMangee != None:
            self.pieceMangeeEn(caseArrivee)
        self.changePosition(caseDepart, caseArrivee)

        # On sauvegarde si il y a toujours echec ou non
        echec = self.echecRoi(couleur)
        # Retour de la piece qui avait bougé
        self.changePosition(caseArrivee, caseDepart)
        # Retour de la piece qui avait ete mangee le cas echeant
        if pieceMangee != None:
            pieceMangee.case = caseArrivee
        # Cas ou on peut sauver l'echec
        if not echec:
            return True
        # Cas ou le mouvement ne sauve pas l'echec
        return False

    #
    # Passe l'attribut enPassant a False pour toutes les pieces adverses
    # Passe l'attribut enPassant de la piece sur @caseArrivee a True si la piece sur caseArrivee est un 
    # pion et a avance de deux cases. 
    # Renvoie True si un pion vient de manger en passant
    #
    def verifieEnPassant(self, caseDepart, caseArrivee, pieceMangee, couleur):
        # Passe l'attribut enPassant a False pour toutes les pieces adverses. On ne peut
        # manger en passant pendant qu'un seul tour 
        for piece in self.pieces:
            if piece.couleur != couleur:
                piece.enPassant = False

        piece = self.pieceSur(caseArrivee)
        # Si la piece qui a bouge est un pion et qu'elle a bouge de deux cases
        if piece != None:
            if piece.nature == PION and abs(caseDepart.ligne - caseArrivee.ligne) == 2:
                piece.enPassant = True
        
        # Un pion vient de manger en passant si pieceMangee est None, 
        # la piece bougee est un pion et ce pion a change de colonne
        if self.pieceSur(caseArrivee) != None:
            if self.pieceSur(caseArrivee).nature == PION and pieceMangee == None and caseDepart.colonne != caseArrivee.colonne:
                if couleur == BLANC:
                    self.pieceMangeeEn(Case(caseArrivee.colonne, caseArrivee.ligne - 1))
                else:
                    self.pieceMangeeEn(Case(caseArrivee.colonne, caseArrivee.ligne + 1))
                return True
        
        return False

    #
    # Renvoie un tableau contenant les cases sur lesquelles la piece sur @caseDepart peut aller
    #
    def movable(self, caseDepart) :
        verifieTypeCase(caseDepart) 
        casesDispos = [] #Valeur renvoyée : tableau des cases vers lesquelles la pièce peut bouger

        #Réécupération de la piece sur la case donnée en argument et de sa nature
        piece = self.pieceSur(caseDepart)

        #Vérifie si la case donnée en argument est bien occupée par une pièce. N'est pas nécessaire pour le moment 
        #cependant, car la méthode est seulement appelée dans move() une fois qu'on a vérifié que la case est occupée
        if piece == None:
            return ValueError("La case donnée en argument n'est occupée par aucune pièce : ", caseDepart)

        #Récupération de la nature, de la case et de la couleur de la pièce 
        nature = piece.nature
        couleur = piece.couleur
        case = piece.case

        # ROI
        if nature == ROI :
            for lig in range(caseDepart.ligne - 1, caseDepart.ligne + 1 + 1) : #range(dep,arr) n'inclut pas arr, on ajoute donc encore 1
                for col in range(caseDepart.colonne - 1, caseDepart.colonne + 1 + 1):
                    if self.caseDisponible(col, lig, couleur) != IMPOSSIBLE:
                        casesDispos.append(Case(col, lig))
            # ROQUES :
            # si roi n'a jamais bouge et n'est pas actuellement en echec
            if not piece.alreadyMoved :
                lig = piece.case.ligne
                # Petit roque
                # Si colonne 5 et 6 sont libres, que  tour colonne 7 n'a bouge
                tour = self.pieceSur(Case(7, lig))
                casesLibres = self.caseDisponible(5, lig, couleur) == LIBRE and self.caseDisponible(6, lig, couleur) == LIBRE
                if tour != None and not tour.alreadyMoved and casesLibres :
                    casesDispos.append(Case(6, lig))
                # Grand roque
                # Si colonne 1, 2 et 3 sont libres, que  tour colonne 0 n'a bouge
                tour = self.pieceSur(Case(0, lig))
                casesLibres = self.caseDisponible(1, lig, couleur) == LIBRE and self.caseDisponible(2, lig, couleur) == LIBRE and self.caseDisponible(3, lig, couleur) == LIBRE
                if tour != None and not tour.alreadyMoved and casesLibres :
                    casesDispos.append(Case(2, lig))

        #DAME
        if nature == DAME:
            self.deplacementVertical(casesDispos, case, couleur)
            self.deplacementDiagonal(casesDispos, case, couleur)
            
        #TOUR
        if nature == TOUR:
            self.deplacementVertical(casesDispos, case, couleur)
            
        #FOU
        if nature == FOU:
            self.deplacementDiagonal(casesDispos, case, couleur)

        # CAVALIER
        if nature == CAVALIER:
            for horizontal in [-2, -1, 1, 2]:
                for vertical in [-2, -1, 1, 2]:
                    if abs(horizontal) != abs(vertical):
                        lig = case.ligne + vertical
                        col = case.colonne + horizontal
                        if self.caseDisponible(col, lig, couleur) != IMPOSSIBLE:
                            casesDispos.append(Case(col, lig))
                        
        # PION
        if nature == PION:
           self.deplacementPion(casesDispos, caseDepart, couleur) 

        return casesDispos
    
    #
    # Renvoie vrai si la piece @piece peut etre mangée en passant
    #
    def enPassant(self, piece):
        piece.enPassant == True

    #
    # Ajoute dans le tableau @casesDipos les cases disponibles pour un pion situe sur 
    # @caseDepart et de couleur @couleur
    #
    def deplacementPion(self, casesDispos, caseDepart, couleur):
        # On n'utilise pas caseDisponible() parce que le pion a des deplacements differents pour
            # manger contrairement a toutes les autres pieces
            
            # Pion blanc :
            if couleur == BLANC:
                # Le pion avance tout droit      
                if coordValides(caseDepart.colonne, caseDepart.ligne + 1):
                    case = Case(caseDepart.colonne, caseDepart.ligne + 1)
                    # Si la case en face du pion n'est pas occupee
                    if self.pieceSur(case) == None:
                        casesDispos.append(case)
                        # Le pion peut avancer de deux cases si il n'a pas encore bouge
                        if caseDepart.ligne == 1:
                            if coordValides(caseDepart.colonne, caseDepart.ligne + 2): 
                                case = Case(caseDepart.colonne, caseDepart.ligne + 2)
                                # Si la case en face situee a deux lignes n'est pas occupee non plus :
                                if self.pieceSur(case) == None:
                                    casesDispos.append(case)

                # Cases en diagonale ne sont dispos que pour manger piece adverse
                if coordValides(caseDepart.colonne - 1, caseDepart.ligne + 1):
                    case = Case(caseDepart.colonne - 1, caseDepart.ligne + 1)
                    piece = self.pieceSur(case) #piece a manger dans cas normal (pas en passant)               
                    #Cas en passant. On regarde si piece a sa droite est un pion qui vient de bouger de deux cases
                    if coordValides(caseDepart.colonne - 1, caseDepart.ligne):
                        caseEnPassant = Case(caseDepart.colonne - 1, caseDepart.ligne)
                        pieceEnPassant = self.pieceSur(caseEnPassant)
                        if pieceEnPassant != None and pieceEnPassant.enPassant:
                                casesDispos.append(case)
                    #Cas mange normal
                    if piece != None and piece.couleur != couleur:
                            casesDispos.append(case)
                if coordValides(caseDepart.colonne + 1, caseDepart.ligne + 1):
                    case = Case(caseDepart.colonne + 1, caseDepart.ligne + 1)
                    piece = self.pieceSur(case) #piece correspondante
                    #Cas en passant. On regarde si piece a sa gauche est un pion qui vient de bouger de deux cases
                    if coordValides(caseDepart.colonne + 1, caseDepart.ligne):
                        caseEnPassant = Case(caseDepart.colonne + 1, caseDepart.ligne)
                        pieceEnPassant = self.pieceSur(caseEnPassant)
                        if pieceEnPassant != None and pieceEnPassant.enPassant:
                                casesDispos.append(case)
                    #Cas mange normal
                    if piece != None and piece.couleur != couleur:
                        casesDispos.append(case)
            
            # Pion noir
            else :
                if coordValides(caseDepart.colonne, caseDepart.ligne - 1):
                    case = Case(caseDepart.colonne, caseDepart.ligne - 1)
                    # Si la case en face du pion n'est pas occupee
                    if self.pieceSur(case) == None:
                        casesDispos.append(case)
                        # Le pion peut avancer de deux cases si il n'a pas encore bouge
                        if caseDepart.ligne == 6:
                            if coordValides(caseDepart.colonne, caseDepart.ligne - 2): 
                                case = Case(caseDepart.colonne, caseDepart.ligne - 2)
                                # Si la case en face situee a deux lignes n'est pas occupee non plus :
                                if self.pieceSur(case) == None:
                                    casesDispos.append(case)
                # Cases en diagonale ne sont dispos que pour manger piece adverse
                if coordValides(caseDepart.colonne - 1, caseDepart.ligne - 1):
                    case = Case(caseDepart.colonne - 1, caseDepart.ligne - 1)
                    piece = self.pieceSur(case) #piece correspondante
                    #Cas en passant. On regarde si piece a sa gauche est un pion qui vient de bouger de deux cases
                    if coordValides(caseDepart.colonne - 1, caseDepart.ligne):
                        caseEnPassant = Case(caseDepart.colonne - 1, caseDepart.ligne)
                        pieceEnPassant = self.pieceSur(caseEnPassant)
                        if pieceEnPassant != None and pieceEnPassant.enPassant:
                                casesDispos.append(case)
                    #Cas mange normal
                    if piece != None and piece.couleur != couleur:
                        casesDispos.append(case)
                if coordValides(caseDepart.colonne + 1, caseDepart.ligne - 1):
                    case = Case(caseDepart.colonne + 1, caseDepart.ligne - 1)
                    piece = self.pieceSur(case) #piece correspondante
                    #Cas en passant. On regarde si piece a sa droite est un pion qui vient de bouger de deux cases
                    if coordValides(caseDepart.colonne + 1, caseDepart.ligne):
                        caseEnPassant = Case(caseDepart.colonne + 1, caseDepart.ligne)
                        pieceEnPassant = self.pieceSur(caseEnPassant)
                        if pieceEnPassant != None and pieceEnPassant.enPassant:
                                casesDispos.append(case)
                    #Cas mange normal
                    if piece != None and piece.couleur != couleur:
                        casesDispos.append(case)

    #
    # Ajoute dans le tableau @casesDipos les cases en diagonales pour une piece situee sur 
    # @caseDepart et de couleur @couleur
    #
    def deplacementDiagonal(self, casesDispos, case, couleur):
        for vertical in [-1,1]:
                for horizontal in [-1, 1]:
                    lig = case.ligne + vertical
                    col = case.colonne + horizontal
                    bloque = False
                    while(coordValides(lig, col) and not bloque):
                        res = self.caseDisponible(col, lig, couleur)
                        if res != IMPOSSIBLE:
                            casesDispos.append(Case(col,lig))
                            # Derniere case accessible dans cette direction, on arrete la recherche de cases dans cette direction
                            if res == MANGE:
                                bloque = True
                        # Case inaccessible, on arrete la le parcours de cases potentielles
                        else:
                            bloque = True
                        #On avance dans la recherche
                        lig += vertical
                        col += horizontal 

    #
    # Ajoute dans le tableau @casesDipos les cases disponibles en vertical pour une piece situee sur 
    # @caseDepart et de couleur @couleur
    #
    def deplacementVertical(self, casesDispos, case, couleur):
        # Deplacement horizontal
            for deplacement in [-1, 1]:
                lig = case.ligne
                col = case.colonne + deplacement
                bloque = False
                while(coordValides(lig, col) and not bloque):
                    res = self.caseDisponible(col, lig, couleur)
                    if res != IMPOSSIBLE:
                        casesDispos.append(Case(col,lig))
                        # Derniere case accessible dans cette direction, on arrete la recherche de cases dans cette direction
                        if res == MANGE:
                            bloque = True
                    # Case inaccessible, on arrete la le parcours de cases potentielles
                    else:
                        bloque = True
                    #On avance dans la recherche
                    col += deplacement 

            # Deplacement vertical
            for deplacement in [-1, 1]:
                lig = case.ligne + deplacement
                col = case.colonne
                bloque = False
                while(coordValides(lig, col) and not bloque):
                    res = self.caseDisponible(col, lig, couleur)
                    if res != IMPOSSIBLE:
                        casesDispos.append(Case(col,lig))
                        # Derniere case accessible dans cette direction, on arrete la recherche de cases dans cette direction
                        if res == MANGE:
                            bloque = True
                    # Case inaccessible, on arrete la le parcours de cases potentielles
                    else:
                        bloque = True
                    #On avance dans la recherche
                    lig += deplacement 

    #
    # Renvoie la piece présente sur la case @case, renvoie None sinon
    #
    def pieceSur(self,case):
        verifieTypeCase(case)

        #Compare la position de chaque piece sur l'echiquier avec la case donnéee en argument
        for piece in self.pieces:
            if piece.case.equalsTo(case) : #and not piece.estMangee(): Ne devrait pas etre nécessaire car @case!="XX"
                return piece
        return None
        """ i=0
        while i < len(self.pieces):
            if self.pieces[i].case.equalsTo(case) :
                return self.pieces[i]
            i += 1
        return None """

    #
    # Renvoie 1 et change l'état de la pièce mangée en @case. Ne fait rien et renvoie 0 sinon
    #
    def pieceMangeeEn(self, case):
        i=0
        while i < len(self.pieces) and not self.pieces[i].case.equalsTo(case):     
            i += 1
        if i == len(self.pieces):
            return 0
        else:
            self.pieces[i].case = Case()
            return 1

    #
    # Transforme le pion passé en @piece
    #
    def transformePionPasse(self, case, piece):
        self.pieceMangeeEn(case)
        self.pieces.append(piece)
    #
    # Change la position de la pièce en @caseDep et renvoie 1. Sinon, ne fait rien et renvoie 0
    #
    def changePosition(self, caseDep, caseArr):
        i=0
        while i < len(self.pieces) and not self.pieces[i].case.equalsTo(caseDep):     
            i += 1
        if i == len(self.pieces):
            return 0
        else:
            self.pieces[i].case = caseArr
            return 1

    #
    # Affiche toutes les pièces présentes sur l'échiquier
    #
    def affiche(self):
        for piece in self.pieces:
            print(piece)

    #
    # Renvoie:
    # -LIBRE si case de coordonnées col,lig est libre pour la pièce de couleur @couleur
    # -MANGE si case de coordonnées col,lig est occupee par une piece adverse
    # -IMPOSSIBLE si piece de même couleur ou coordonnées (col,lig) incorrectes
    #
    def caseDisponible(self, col, lig, couleur):
        if not coordValides(lig, col):
            return IMPOSSIBLE
        piece=self.pieceSur(Case(col, lig))
        if piece == None :
            return LIBRE
        else:
            if piece.couleur == couleur:
                return IMPOSSIBLE
            else:
                return MANGE

    #
    # Renvoie vrai si le roi de la couleur donnée  en argument est en echec
    #
    def echecRoi(self, couleur):
        # On recupere la case du roi
        for piece in self.pieces:
            if piece.nature == ROI and piece.couleur == couleur:
                caseRoi = piece.case
                # pas besoin de parcourir plus loin, on a trouve le roi
                break

        #On regarde si une des pieces de couleur adverse peut bouger sur cette case
        for piece in self.pieces:
            if piece.couleur != couleur:
                for case in self.movable(piece.case):
                    if case.equalsTo(caseRoi):
                        return True        

        # On a parcouru toutes les pieces sans qu'aucune ne donne d'echec au roi adverse
        return False

    #
    # Renvoie la case du roi de couleur donnee en argument
    #
    def caseRoi(self, couleur):
        for piece in self.pieces:
            if piece.nature == ROI and piece.couleur == couleur:
                return piece.case

    #
    # Renvoie vrai si le roi de couleur donnee en argument est en echec et mat
    #
    def echecMat(self, couleur):
        # Si le roi de coueur @couleur n'est pas en echec
        if not self.echecRoi(couleur):
            return False

        # Si le roi est en echec :
        # parcours des pieces de couleur @couleur 
        for piece in self.pieces:
            if piece.couleur == couleur and not piece.estMangee():
                caseDepart = piece.case
                # On teste tous les mouvements possibles de la piece
                for caseArrivee in self.movable(caseDepart):
                    if self.moveEchecMat(caseDepart, caseArrivee, couleur):
                        """ TESTS :
                        print("-" + str(piece))
                        print(str(caseDepart) + " " + str(caseArrivee))
                        """
                        return False

        #Aucun mouvement n'a empeche l'echec
        return True
