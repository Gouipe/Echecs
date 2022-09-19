from operator import mod
import pygame
from pygame.locals import *
from constantes import *
from graphique import *
from case import *
from echiquier import *

#
# Renvoie la case sélectionnée par la souris (il faut donner en argument
# l'attribut pos de l'event du click de la souris)
# pos est un tuple de forme (x,y)
#       
def caseSelectionnee(pos) :
	try:
		return Case(pos[0] // SQUARE, pos[1] // SQUARE)
	except ValueError:
		return None
	
#
# Renvoie la nature de la piece sélectionnée en cas de pion passé
#
def pieceSelectionnee(pos) :
	#print('piece selectionnee : x=' + str(pos[0]) + ' y=' + str(pos[1]))
	#selection invalide
	if pos[0] < BOARD_SIZE or pos[1] > PIECE_DIM :
		return None

	# selection valide
	x = BOARD_SIZE + PIECE_DIM
	if pos[0] < x :
		return DAME

	x += PIECE_DIM
	if pos[0] < x :
		return TOUR

	x += PIECE_DIM
	if pos[0] < x :
		return FOU

	return CAVALIER

def main():
	pygame.init()
	fenetre = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	echiquier = Echiquier()
	graphique = Graphique(echiquier, fenetre)
	graphique.affichePieces()
	couleur = BLANC # A blanc de jouer au depart
	etat = CHOISIR_PIECE # Etat initial est choisir une piece

	continuer = 1
	while continuer:
		

		for event in pygame.event.get():   #On parcoure la liste de tous les événements reçus
			if event.type == QUIT:     #Si un de ces événements est de type QUIT
				continuer=0
			if event.type == MOUSEBUTTONDOWN and event.button == 1 :
				print('etat:' + str(etat))
				if etat == CHOISIR_PIECE :
					caseDep = caseSelectionnee(event.pos)
					if caseDep != None:
						piece = echiquier.pieceSur(caseDep)
						# Si on a choisi une piece de la bonne couleur, on passe  a l'etat suivant
						if piece != None and piece.couleur == couleur:
							graphique.surligne(caseDep)
							etat = CHOISIR_ARRIVEE
					break

				if etat == CHOISIR_ARRIVEE :
					caseArr = caseSelectionnee(event.pos)
					if caseArr != None:
						resMove = echiquier.move(caseDep, caseArr, couleur)

						# Cas déplacement piece normal
						if resMove == MOVED :
							# Met a jour graphiquement les cases de depart, d'arrivee et celle du roi
							# au cas ou elle etait devenu rouge a cause d'un echec non vu 
							graphique.afficheCase(caseDep)
							graphique.afficheCase(caseArr)
							graphique.afficheCase(echiquier.caseRoi(couleur))
							couleur = (couleur + 1) % 2 # on change de couleur

						# Cas déplacement en roque
						if resMove == ROQUE:
							for col in range(8):
								graphique.afficheCase(Case(col, caseArr.ligne))
							couleur = (couleur + 1) % 2 # on change de couleur

						# Cas déplacement en passant
						if resMove == EN_PASSANT:
							graphique.afficheCase(caseDep)
							graphique.afficheCase(caseArr)

							#La piece mangee est une ligne avant ou apres la case d'arrivee selon
							# si la piece mangee est blanche ou noire
							graphique.afficheCase(Case(caseArr.colonne, caseArr.ligne - 1))
							graphique.afficheCase(Case(caseArr.colonne, caseArr.ligne + 1))
							couleur = (couleur + 1) % 2 # on change de couleur

						
						if echiquier.echecMat(couleur):
							#continuer = 0
							print("echec et mat")
							#AFFICHER RESULTAT
						
						# Cas deplacement piece impossible a cause d'echec
						if resMove == CHECK:
							caseRoi = echiquier.caseRoi(couleur)
							graphique.afficheCaseRouge(caseRoi)			
						
						# nouvel etat hors cas pion passé
						etat = CHOISIR_PIECE

						if resMove == PION_PASSE:
							graphique.afficheCase(caseDep)
							etat = TRANSFORMATION_PION
							#AFFICHIER CHOIX
							graphique.afficherChoixPionPasse(couleur)

					graphique.afficheCase(caseDep)
					break

				if etat == TRANSFORMATION_PION:
					#SELECTIONNER CHOIX
					nature = pieceSelectionnee(event.pos)

					# le joueur a choisi la nouvelle piece:
					if nature != None:
						#TRANSFORMER PION
						piece = Piece(couleur, nature, caseArr)
						echiquier.transformePionPasse(caseArr, piece)
						graphique.afficheCase(caseArr)
						#EFFACER CHOIX
						#TODO
						couleur = (couleur + 1) % 2 # on change de couleur
						etat = CHOISIR_PIECE
					break
main()

