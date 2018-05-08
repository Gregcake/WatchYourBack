import math
import random
import time
from heuristic  import Heuristic
from copy import deepcopy

WHITE = "O"
BLACK = "@"
CORNER = "X"
EMPTY = "-"
DEBUG = False
MAX_DEPTH = 2
CENTER = 3.5

class Strategy:
	def __init__(self):
		pass

	def placement(self, board, color):
		if DEBUG:
			x = int(input())
			y = int(input())
			return (x,y)
		else:
			potential_boards = []
			for placement in board.available_placements(color):
				potential_board = deepcopy(board)
				potential_board.place(color, placement)
				potential_boards.append((self.placement_AB(potential_board, 0, -math.inf, math.inf, board.enemy), placement))
			return max(potential_boards)[1]

	def placement_AB(self, board, depth, a, b, color):
		if board.player_pieces <= 2 or depth == MAX_DEPTH:
			return Heuristic(board)
		if color == board.player:
			v = -math.inf
			for placement in board.available_placements(color):
				potential_board = deepcopy(board)
				potential_board.place(color, placement)
				v = max(v, self.placement_AB(potential_board, depth+1, a, b, board.enemy))
				a = max(a, v)
				if b <= a:
					break
			return v
		else:
			v = math.inf
			for placement in board.available_placements(color):
				potential_board = deepcopy(board)
				potential_board.place(color, placement)
				v = min(v, self.placement_AB(potential_board, depth+1, a, b, board.player))
				b = min(b, v)
				if b <= a:
					break
			return v

	def movement(self, board, color):
		if DEBUG:
			x = int(input())
			y = int(input())
			pos_from = (x,y)
			x = int(input())
			y = int(input())
			pos_to = (x,y)
			return (pos_from, pos_to)
		else:
			potential_boards = []
			for move in board.available_moves(color):
				potential_board = deepcopy(board)
				potential_board.move(color, move[0], move[1])
				potential_boards.append((self.movement_AB(potential_board, 0 , -math.inf, math.inf, board.enemy), move))
			return max(potential_boards)[1]

	def movement_AB(self, board, depth, a, b, color):
		if board.player_pieces <= 2 or depth == MAX_DEPTH:
			return Heuristic(board)
		if color == board.player:
			v = -math.inf
			for move in board.available_moves(color):
				potential_board = deepcopy(board)
				potential_board.move(color, move[0], move[1])
				v = max(v, self.movement_AB(potential_board, depth+1, a, b, board.enemy))
				a = max(a, v)
				if b <= a:
					break
			return v
		else:
			v = math.inf
			for move in board.available_moves(color):
				potential_board = deepcopy(board)
				potential_board.move(color, move[0], move[1])
				v = min(v, self.movement_AB(potential_board, depth+1, a, b, board.player))
				b = min(b, v)
				if b <= a:
					break
			return v
		