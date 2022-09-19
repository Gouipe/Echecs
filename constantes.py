"""DIMENSIONS"""
SQUARE = 45 # dimension d'une case
WINDOW_HEIGHT = SQUARE*8
SIDE_BAR = 180
WINDOW_WIDTH = SQUARE*8 + SIDE_BAR
BOARD_SIZE = 8 * SQUARE
PIECE_DIM = 45

"""TUPLES COULEUR"""
WHITE_SQUARE_COLOR = (200,200,200)
BLACK_SQUARE_COLOR = (50, 200, 200)
RED_SQUARE_COLOR = (220, 0, 60)
SELECTED_COLOR = (255,255,255)
SIDE_BAR_COLOR = (100,100,100)

"""PIECES"""
ROI = 0
DAME = 1
TOUR = 2
FOU = 3
CAVALIER = 4
PION = 5

"""RESULTATS MOVE()"""
AUCUNE_PIECE = 0
MOVED = 1
CHECK = 2
MAUVAISE_COULEUR = 3
IMPOSSIBLE = 4
EN_PASSANT = 5
CHECKMATE = 6
ROQUE = 7
PION_PASSE = 8

"""EVENT"""

"""RESULTATS CASEDISPONIBLE()"""
LIBRE = 0
MANGE = 1

"""AUTRE"""
NOIR = 0
BLANC = 1

"""AUTOMATE"""
CHOISIR_PIECE = 0
CHOISIR_ARRIVEE = 1
TRANSFORMATION_PION = 3
