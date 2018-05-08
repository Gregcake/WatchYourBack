import math
from random import randint

CENTER = 3.5
CORNER = "X"
EMPTY = "-"

class Heuristic:
	def __init__(self, board):
		self.board = board

	def __lt__(self, other):
		if other == -math.inf:
			return False
		elif other == math.inf:
			return True
		return (pieces_remaining(self.board),pieces_vulnerable(self.board), density(self.board), randint(0,9)) < (pieces_remaining(other.board),pieces_vulnerable(other.board), density(other.board), randint(0,9))
	def __gt__(self, other):
		if other == -math.inf:
			return True
		elif other == math.inf:
			return False
		return (pieces_remaining(self.board),pieces_vulnerable(self.board), density(self.board), randint(0,9)) > (pieces_remaining(other.board),pieces_vulnerable(other.board), density(other.board), randint(0,9))
	def __eq__(self, other):
		if other == -math.inf:
			return False
		elif other == math.inf:
			return False
		return (pieces_remaining(self.board),pieces_vulnerable(self.board), density(self.board), randint(0,9)) == (pieces_remaining(other.board),pieces_vulnerable(other.board), density(other.board), randint(0,9))
	def __le__(self, other):
		if other == -math.inf:
			return False
		elif other == math.inf:
			return True
		return (pieces_remaining(self.board),pieces_vulnerable(self.board), density(self.board), randint(0,9)) <= (pieces_remaining(other.board),pieces_vulnerable(other.board), density(other.board), randint(0,9))
	def __ge__(self, other):
		if other == -math.inf:
			return True
		elif other == math.inf:
			return False
		return (pieces_remaining(self.board),pieces_vulnerable(self.board), density(self.board), randint(0,9)) >= (pieces_remaining(other.board),pieces_vulnerable(other.board), density(other.board), randint(0,9))
	def __ne__(self, other):
		if other == -math.inf:
			return True
		elif other == math.inf:
			return True
		return (pieces_remaining(self.board),pieces_vulnerable(self.board), density(self.board), randint(0,9)) != (pieces_remaining(other.board),pieces_vulnerable(other.board), density(other.board), randint(0,9))


def pieces_remaining(board):
	return board.player_pieces-board.enemy_pieces

def pieces_vulnerable(board):
	vulnerable = 0
	for y in range(len(board.grid)):
		for x in range(len(board.grid[y])):
			piece = board.grid[y][x]
			if piece == board.player:
				try:
					north = board.grid[y-1][x]
					south = board.grid[y+1][x]
					if ((north == board.enemy or north == CORNER) and (south == EMPTY) and (y-1>=0)):
						vulnerable+= 1
				except:
					pass
				try:
					north = board.grid[y-1][x]
					south = board.grid[y+1][x]
					if ((south == board.enemy or south == CORNER) and (north == EMPTY) and (y-1>=0)):
						vulnerable+= 1
				except:
					pass
				try:
					west = board.grid[y][x-1]
					east = board.grid[y][x+1]
					if ((west == board.enemy or west == CORNER) and (east == EMPTY) and (x-1>=0)):
						vulnerable+= 1
				except:
					pass
				try:
					west = board.grid[y][x-1]
					east = board.grid[y][x+1]
					if ((east == board.enemy or east == CORNER) and (west == EMPTY) and (x-1>=0)):
						vulnerable+= 1
				except:
					pass
	return -vulnerable

def density(board):
	d = 0
	p = 0
	for y in range(len(board.grid)):
		for x in range(len(board.grid[y])):
			piece = board.grid[y][x]
			if piece == board.player:
				p+= 1
				d+= math.sqrt((abs(y-CENTER)**2)+(abs(x-CENTER)**2))
	if p == 0:
		return 0
	else:
		d/= p
		return -d