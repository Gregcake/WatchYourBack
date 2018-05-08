import math

WHITE = "O"
BLACK = "@"
CORNER = "X"
EMPTY = "-"

class Strategy:
	def __init__(self):
		pass

	def placement(board, t):
		pass

	def movement(board, t):
		minmaxAB_movement(board, 0, -math.inf, math.inf, board.player)

	def minmaxAB_movement(board, depth, a, b, color):
		if depth == 0 or (if color == WHITE and board.white <= 2) or (if color == BLACK and board.black <= 2):
			return (board.white, board.black)


