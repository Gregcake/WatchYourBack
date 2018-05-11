import math
from random import randint

CENTER = 3.5
CORNER = "X"

class Heuristic:
	def __init__(self, board):
		self.board = board

	def __lt__(self, other):
		if other == -math.inf:
			return False
		elif other == math.inf:
			return True
		return (pieces_remaining(self.board),exposure(self.board), density(self.board), randint(0,12)) < (pieces_remaining(other.board),exposure(other.board), density(other.board), randint(0,12))
	def __gt__(self, other):
		if other == -math.inf:
			return True
		elif other == math.inf:
			return False
		return (pieces_remaining(self.board),exposure(self.board), density(self.board), randint(0,12)) > (pieces_remaining(other.board),exposure(other.board), density(other.board), randint(0,12))
	def __eq__(self, other):
		if other == -math.inf:
			return False
		elif other == math.inf:
			return False
		return (pieces_remaining(self.board),exposure(self.board), density(self.board), randint(0,12)) == (pieces_remaining(other.board),exposure(other.board), density(other.board), randint(0,12))
	def __le__(self, other):
		if other == -math.inf:
			return False
		elif other == math.inf:
			return True
		return (pieces_remaining(self.board),exposure(self.board), density(self.board), randint(0,12)) <= (pieces_remaining(other.board),exposure(other.board), density(other.board), randint(0,12))
	def __ge__(self, other):
		if other == -math.inf:
			return True
		elif other == math.inf:
			return False
		return (pieces_remaining(self.board),exposure(self.board), density(self.board), randint(0,12)) >= (pieces_remaining(other.board),exposure(other.board), density(other.board), randint(0,12))
	def __ne__(self, other):
		if other == -math.inf:
			return True
		elif other == math.inf:
			return True
		return (pieces_remaining(self.board),exposure(self.board), density(self.board), randint(0,12)) != (pieces_remaining(other.board),exposure(other.board), density(other.board), randint(0,12))


def pieces_remaining(board):
	return (board.player_pieces,-board.enemy_pieces)

def exposure(board):
	vulnerability = 0
	pieces = 0
	for pos in board.grid:
		if board.grid[pos] == board.player:
			pieces+= 1
			x = pos[0]
			y = pos[1]
			if (board.grid.get((x,y-1)) == board.enemy or board.grid.get((x,y-1)) == CORNER) and (x,y+1) not in board.grid and board.within_bounds((x,y+1)):
				vulnerability+= 1
			if (board.grid.get((x,y+1)) == board.enemy or board.grid.get((x,y+1)) == CORNER) and (x,y-1) not in board.grid and board.within_bounds((x,y-1)):
				vulnerability+= 1
			if (board.grid.get((x+1,y)) == board.enemy or board.grid.get((x+1,y)) == CORNER) and (x-1,y) not in board.grid and board.within_bounds((x-1,y)):
				vulnerability+= 1
			if (board.grid.get((x-1,y)) == board.enemy or board.grid.get((x-1,y)) == CORNER) and (x+1,y) not in board.grid and board.within_bounds((x+1,y)):
				vulnerability+= 1
	if pieces == 0:
		return 0
	else:
		vulnerability/= pieces
		return -vulnerability

def density(board):
	density = 0
	pieces = 0
	for pos in board.grid:
		if board.grid[pos] == board.player:
			density+= math.sqrt((abs(pos[0]-CENTER)**2)+(abs(pos[1]-CENTER)**2))
			pieces+=1
	if pieces == 0:
		return 0
	else:
		density/= pieces
		return -density