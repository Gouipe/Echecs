from operator import mod
import pygame
from pygame.locals import *
from constantes import *
from echiquier import *

class Graphique:

    def __init__(self, echiquier, fenetre):
        #ATTRIBUTS
        self.echiquier = echiquier
        self.fenetre = fenetre

    #
    # Affiche toutes les cases de l'echiquier sans les pieces
    #
    def afficherFenetre(self):
        white=0 #couleur de la case courante
        for x in range(8) : #Chess board is 8x8 cases
            white = (white + 1) % 2
            for y in range(8):
                if white :
                    self.afficheFondBlanc(x,y)      
                else : 
                    self.afficheFondNoir(x,y)
                white = (white + 1) % 2 #changement de couleur
        self.afficheSideBar()
        pygame.display.flip()

    def afficheSideBar(self):
        square = pygame.Rect(BOARD_SIZE, 0, SIDE_BAR, WINDOW_HEIGHT)
        pygame.draw.rect(self.fenetre, SIDE_BAR_COLOR, square)

    #
    # Affiche les choix de pieces possibles de transformation pour un pion
    # passe de couleur @couleur
    #
    def afficherChoixPionPasse(self, couleur):
        decalage = PIECE_DIM
        x = BOARD_SIZE
        y = 0

        # Pion passe blanc
        if couleur == BLANC:
            for piece in [Piece(BLANC, DAME), Piece(BLANC, TOUR), Piece(BLANC, FOU), Piece(BLANC, CAVALIER)]:    
                # RECUPERATION DU NOM DU FICHIER CORRESPONDANT A  LA PIECE
                fileName = self.getFileName(piece)
                # AFFICHAGE DE LA PIECE
                imagePiece = pygame.image.load("./images/" + fileName + ".svg").convert_alpha()
                self.fenetre.blit(imagePiece,(x, y))
                x = x + decalage
        
        # Pion passe noir
        else:
            for piece in [Piece(NOIR, DAME), Piece(NOIR, TOUR), Piece(NOIR, FOU), Piece(NOIR, CAVALIER)]:    
                # RECUPERATION DU NOM DU FICHIER CORRESPONDANT A  LA PIECE
                fileName = self.getFileName(piece)
                # AFFICHAGE DE LA PIECE
                imagePiece = pygame.image.load("./images/" + fileName + ".svg").convert_alpha()
                self.fenetre.blit(imagePiece,(x, y))
                x = x + decalage

        # Affichage resultat
        pygame.display.flip()

    #
    # Affiche toutes les pieces de l'echiquier (fond + piece)
    # 
    def affichePieces(self) :
        #Reinitialisation du board pour effacer toutes les pieces
        self.afficherFenetre()
        # parcours des pieces de l'echiquier
        for piece in self.echiquier.pieces :
            if not piece.estMangee():
                # RECUPERATION DU NOM DU FICHIER CORRESPONDANT A  LA PIECE
                fileName = self.getFileName(piece)

                # AFFICHAGE DE LA PIECE
                imagePiece = pygame.image.load("./images/" + fileName + ".svg").convert_alpha()
                self.fenetre.blit(imagePiece,(piece.case.colonne * SQUARE, piece.case.ligne * SQUARE))
        pygame.display.flip()

    #
    #Affiche la piece qui est sur la case donnee en argument
    #
    def affichePiece(self, case):
        piece = self.echiquier.pieceSur(case)
        if not piece.estMangee():
            # RECUPERATION DU NOM DU FICHIER CORRESPONDANT A  LA PIECE
            fileName = self.getFileName(piece)

            # AFFICHAGE DE LA PIECE
            imagePiece = pygame.image.load("./images/" + fileName + ".svg").convert_alpha()
            self.fenetre.blit(imagePiece,(piece.case.colonne * SQUARE, piece.case.ligne * SQUARE))
        pygame.display.flip()  


    #
    # Affiche la case donnée en argument (fond + piece)
    #
    def afficheCase(self, case):
        # Affiche le fond de la case
        if (case.colonne % 2 == 0 and case.ligne % 2 == 0) or (case.colonne % 2 == 1 and case.ligne % 2 == 1) :
            self.afficheFondBlanc(case.colonne, case.ligne)
        else:
            self.afficheFondNoir(case.colonne, case.ligne)

        # Affiche la piece de la case si elle existe
        piece = self.echiquier.pieceSur(case)
        if piece != None:
            # Recuperation du nom du fichier cspdt a la piece
            fileName = self.getFileName(piece)
            # Affichage de la piece
            imagePiece = pygame.image.load("./images/" + fileName + ".svg").convert_alpha()
            self.fenetre.blit(imagePiece,(piece.case.colonne * SQUARE, piece.case.ligne * SQUARE))
        
        # Actualise le changement
        pygame.display.flip()

    #
    # Affiche un fond rouge rouge et la piece associée à la case (col,lig)
    #
    def afficheCaseRouge(self, case):
        self.afficheFondRouge(case.colonne, case.ligne)
        self.affichePiece(case)

    #
    # Affiche un fond rouge vert et la piece associée à la case (col,lig)
    #
    def afficheCaseVert(self, case):
        self.afficheFondVert(case.colonne, case.ligne)
        self.affichePiece(case)

    def surligne(self, case):
        self.afficheFondSurligne(case.colonne, case.ligne)
        self.affichePiece(case)

    #
    # Colorie la case correspondant aux arguments (col,lig) en rouge
    #
    def afficheFondRouge(self, col, lig):
        square = pygame.Rect(col * SQUARE, lig * SQUARE, SQUARE, SQUARE)
        pygame.draw.rect(self.fenetre, RED_SQUARE_COLOR, square)

    #
    # Colorie la case correspondant aux arguments (col,lig) en vert
    #
    def afficheFondVert(self, col, lig):
        square = pygame.Rect(col * SQUARE, lig * SQUARE, SQUARE, SQUARE)
        pygame.draw.rect(self.fenetre, GREEN_SQUARE_COLOR, square)

    #
    # Colorie la case correspondant aux arguments (col,lig) en blanc
    #
    def afficheFondBlanc(self, col, lig):
        square = pygame.Rect(col * SQUARE, lig * SQUARE, SQUARE, SQUARE)
        pygame.draw.rect(self.fenetre, WHITE_SQUARE_COLOR, square)

    def afficheFondSurligne(self, col, lig):
        square = pygame.Rect(col * SQUARE, lig * SQUARE, SQUARE, SQUARE)
        pygame.draw.rect(self.fenetre, SELECTED_COLOR, square)

    #
    # Colorie la case correspondant aux arguments (col,lig) en noir
    #
    def afficheFondNoir(self, col, lig):
        square = pygame.Rect(col * SQUARE, lig * SQUARE, SQUARE, SQUARE)
        pygame.draw.rect(self.fenetre, BLACK_SQUARE_COLOR, square)

    #
    # Colorie les cases protégées par la piece sur la case donnee en argument en vert,
    # celles attaquées en rouge, et remplit les autres casses possibles  vides avec petit logo.
    # Renvoie un tableau des cases modifiées pour pouvoir rétablir leur aspect normal ensuite
    #
    def afficheAide(case): # ou col,lig
        pass

    #
    # Récupère le nom du fichier correspondant a la piece
    #
    def getFileName(self, piece) :
        # Valeur renvoyee
        pieceFichier = "Chess_"

        # Concatenation de la nature de la piece
        if piece.nature == ROI :
            pieceFichier += 'k'
        else :
            if piece.nature == DAME :
                pieceFichier += 'q'
            else :
                if piece.nature == TOUR :
                    pieceFichier += 'r'
                else :
                    if piece.nature == FOU :
                        pieceFichier += 'b'
                    else :
                        if piece.nature == CAVALIER :
                            pieceFichier += 'n'
                        else :
                            pieceFichier += 'p'

        #Concatenation de la couleur de la piece
        if piece.couleur == BLANC :
            pieceFichier += 'l' #light
        else :
            pieceFichier += 'd' #dark

        # Fin commune a tous les fichiers
        pieceFichier += "t45"

        return pieceFichier
