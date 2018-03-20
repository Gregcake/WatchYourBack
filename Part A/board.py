import copy
import random
from operator import attrgetter

WHITE = "O"
BLACK = "@"
CORNER = "X"
EMPTY = "-"
DEPTH_LIMIT = 5

class Board:
	def __init__(self):
		# 2D Array representation of board state
		self.grid = []
		# Number of white and black pieces on the board in current state
		self.white = 0
		self.black = 0
		self.moves = []

	def read_from_stdin(self, board_size):
		for i in range(board_size):
			row = list(input())
			# Tally white and black pieces on the board
			for space in row:
				if space == WHITE:
					self.white+= 1
				elif space == BLACK:
					self.black+= 1
			self.grid.append(row)

	def available_moves(self, player):
		moves = {}
		for row in range(len(self.grid)):
			for col in range(len(self.grid[row])):
				if self.grid[row][col] == player:
					#Check available moves for piece at (row,col)
					possible_moves = self.check_moves(row, col)
					moves[(row,col)] = possible_moves
		return moves

	def check_moves(self, row, col):
		moves = []
		#Check north
		try:
			#Check adjacent
			if self.grid[row-1][col] == EMPTY:
				moves.append((row-1,col))
			#Adjacent occupied, check if jump available
			elif self.grid[row-2][col] == EMPTY:
				moves.append((row-2,col))
		except:
			pass
		#Check south
		try:
			if self.grid[row+1][col] == EMPTY:
				moves.append((row+1,col))
			elif self.grid[row+2][col] == EMPTY:
				moves.append((row+2,col))
		except:
			pass
		#Check west
		try:
			if self.grid[row][col-1] == EMPTY:
				moves.append((row,col-1))
			elif self.grid[row][col-2] == EMPTY:
				moves.append((row,col-2))
		except:
			pass
		#Check east
		try:
			if self.grid[row][col+1] == EMPTY:
				moves.append((row,col+1))
			elif self.grid[row][col+2] == EMPTY:
				moves.append((row,col+2))
		except:
			pass
		random.shuffle(moves)
		return moves

	def check_eliminated(self, row, col):
		piece = self.grid[row][col]
		enemy = opposite(piece)
		try:
			north = self.grid[row-1][col]
			south = self.grid[row+1][col]
			if((north == enemy or north == CORNER) and (south == enemy or south == CORNER)):
				return True
		except:
			pass
		try:
			east = self.grid[row][col-1]
			west = self.grid[row][col+1]
			if((east == enemy or east == CORNER) and (west == enemy or west == CORNER)):
				return True
		except:
			pass
		return False

	def move(self, pos_from, pos_to):
		piece = self.grid[pos_from[0]][pos_from[1]]
		self.grid[pos_to[0]][pos_to[1]] = piece
		self.grid[pos_from[0]][pos_from[1]] = EMPTY
		self.moves.append((pos_from, pos_to))
		# Refresh board, eliminating enemy pieces
		self.refresh(opposite(piece))
		# Refresh board, check for sucides
		self.refresh(piece)

	def refresh(self, piece):
		for row in range(len(self.grid)):
			for col in range(len(self.grid)):
				if self.grid[row][col] == piece:
					if self.check_eliminated(row, col):
						self.grid[row][col] = EMPTY
						if piece == BLACK:
							self.black-= 1
						elif piece == WHITE:
							self.white-= 1

	def massacre(self):
		depth = 0
		board_states = []
		board_states.append(self)
		while depth < DEPTH_LIMIT:
			possible_states = []
			for board in board_states:
				if board.black == 0:
					depth = DEPTH_LIMIT
					possible_states.append(board)
					pass
				else:
					moves = board.available_moves(WHITE)
					for pos_from in moves:
						for pos_to in moves[pos_from]:
							possible_board = copy.deepcopy(board)
							possible_board.move(pos_from, pos_to)
							possible_states.append(possible_board)
			board_states = possible_states
			depth+= 1

		min_moves = DEPTH_LIMIT+len(self.moves)
		min_black = self.black
		optimal = False
		check = []
		for board in board_states:
			check.append(len(board.moves))
		print(set(check))
		self = copy.deepcopy(min(board_states,key=attrgetter('black','moves')))
		print(self.black)
		return self



def opposite(piece):
	if piece == WHITE:
		return BLACK
	elif piece == BLACK:
		return WHITE