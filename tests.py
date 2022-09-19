from operator import mod
import pygame
from pygame.locals import *
from constantes import *
from case import *
from echiquier import *


"""--------------TESTS--------------"""
res=0 #variable dans laquelle on va mettre les résultats des méthodes testées
echiquier = Echiquier()

"""------------------------------------PETITS TESTS--------------------------------------"""
#echiquier.affiche()
#echiquier.movable(Case('D',1))
#print("Coordonnées normalisées de D1 : ",Case('D',1).getColNorm(), Case('D',1).getLigNorm())
#print("Coordonnées non normalisées de (3, 0) : ", toNNCol(3), toNNLine(0))
print(echiquier.movable(Case('E', 1)))
print(echiquier.pieceSur(Case('E', 2)))
pion=echiquier.pieceSur(Case('E', 2))
print(echiquier.move(Case('E', 1), Case('E', 2), BLANC))
print(echiquier.pieceSur(Case('E', 1)))
print(echiquier.pieceSur(Case('E', 2)))
print(pion.case)
#print(echiquier.move(Case('E', 1), Case('F',1)))
"""--------------------------------------------------------------------------------------"""

piece = echiquier.pieceSur(Case('F', 1))
res = piece.equalsTo(Piece(BLANC, FOU, Case('F',1)))
if not res :
    print("problème avec : piece.equalsTo(Piece(BLANC, FOU, Case('F',1))). Renvoie ", res, " au lieu de 'True'")



res=echiquier.move(Case('E', 1), Case('A',1), BLANC)
if res != IMPOSSIBLE :
    print("problème avec : echiquier.move(Case('E', 1), Case('A',1))). Renvoie ", res," au lieu de ",IMPOSSIBLE)
"""------------FIN TESTS------------"""
