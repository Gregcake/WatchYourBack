'''
Written by Greg Tan (726323) & Luis Adjero (762095)
COMP30024: Artificial Intelligence
Project Part A: Massacre
Last Edited 22/03/2018

Board Class Definition
'''

import copy
import random
from operator import attrgetter

WHITE = "O"
BLACK = "@"
CORNER = "X"
EMPTY = "-"
DEPTH_LIMIT = 4

class Board:

	# Initialize board object instance
	def __init__(self):
		# 2D Array representation of board state
		self.grid = []
		# Number of white and black pieces on the board in current state
		self.white = 0
		self.black = 0
		# History of moves required to reach current state
		self.moves = []

	# Given a board size, initialize the bord of matching size from stdin
	def read_from_stdin(self, board_size):
		for i in range(board_size):
			row = input().split(' ')
			# Tally white and black pieces on the board
			for space in row:
				if space == WHITE:
					self.white+= 1
				elif space == BLACK:
					self.black+= 1
			# Push row into ith row of grid object
			self.grid.append(row)

	# Given a piece, return a dict of all available moves for piece type
	def available_moves(self, player):
		# Available moves are represented by a dict:
		#		 key : valye
		# 	  origin : [north, south, west] 
		# (row, col) : [(row, col), (row, col), (row, col)]
		moves = {}
		# Iterate through each square on the grid,
		# If square == WHITE/BLACK, add list of available moves
		for row in range(len(self.grid)):
			for col in range(len(self.grid[row])):
				if self.grid[row][col] == player:
					#Check available moves for piece at (row,col)
					possible_moves = self.check_moves(row, col)
					moves[(row,col)] = possible_moves
		return moves

	# Given a row,col, return a list of available squares that piece can move to
	def check_moves(self, row, col):
		moves = []
		# Check north
		try:
			# Check adjacent, block negative indexing
			if self.grid[row-1][col] == EMPTY and row-1>=0:
				moves.append((row-1,col))
			# Check if jump available, block negative indexing
			elif self.grid[row-2][col] == EMPTY and row-2>=0:
				moves.append((row-2,col))
		except:
			pass
		# Check south
		try:
			# Check adjacent, catch index out of bounds errors
			if self.grid[row+1][col] == EMPTY:
				moves.append((row+1,col))
			elif self.grid[row+2][col] == EMPTY:
				moves.append((row+2,col))
		except:
			pass
		# Check west
		try:
			if self.grid[row][col-1] == EMPTY and col-1>=0:
				moves.append((row,col-1))
			elif self.grid[row][col-2] == EMPTY and col-2>=0:
				moves.append((row,col-2))
		except:
			pass
		# Check east
		try:
			if self.grid[row][col+1] == EMPTY:
				moves.append((row,col+1))
			elif self.grid[row][col+2] == EMPTY:
				moves.append((row,col+2))
		except:
			pass
		# Randomize order of moves
		# Should no solution be found, no bias towards a single direction
		random.shuffle(moves)
		return moves

	# Given a row,col, check if the piece on that square is eliminated
	# True if eliminated, false otherwise
	def check_eliminated(self, row, col):
		# Determine color of piece we're checking to eliminate and it's opposite
		piece = self.grid[row][col]
		enemy = opposite(piece)

		# Check vertical and horizontal axis, if piece is cornered return true
		# Use try blocks for each axis to catch index OOB errors on grid
		try:
			north = self.grid[row-1][col]
			south = self.grid[row+1][col]
			if((north == enemy or north == CORNER) and
				(south == enemy or south == CORNER)):
				return True
		except:
			pass
		try:
			east = self.grid[row][col-1]
			west = self.grid[row][col+1]
			if((east == enemy or east == CORNER) and 
				(west == enemy or west == CORNER)):
				return True
		except:
			pass
		# Piece not cornered
		return False

	# Given a two row,col positions, move a piece at pos_from to pos_to
	def move(self, pos_from, pos_to):
		# Determine type of piece to move
		# Replace destination with piece and empty origin
		piece = self.grid[pos_from[0]][pos_from[1]]
		self.grid[pos_to[0]][pos_to[1]] = piece
		self.grid[pos_from[0]][pos_from[1]] = EMPTY
		# Add to history of moves for this board
		self.moves.append((pos_from, pos_to))
		# Refresh board, eliminating enemy pieces
		self.refresh(opposite(piece))
		# Refresh board, check for sucides
		# (Elimination priority to player that moved)
		self.refresh(piece)

	# Given a piece type, check the board for pieces to be eliminated
	def refresh(self, piece):
		# Scan board for pieces that should be eliminated in current state
		for row in range(len(self.grid)):
			for col in range(len(self.grid)):
				if self.grid[row][col] == piece:
					if self.check_eliminated(row, col):
						# Piece eliminated
						# Empty occupying square and deduct piece type count
						self.grid[row][col] = EMPTY
						if piece == BLACK:
							self.black-= 1
						elif piece == WHITE:
							self.white-= 1

	# Return a sequence of moves for white pieces to eliminate all black pieces
	def massacre(self):
		depth = 0
		optimal_cycle = False
		# Potential boards are held in a list of board objects
		# Load current state to begin
		board_states = []
		board_states.append(self)
		# Limited minmax algorithm, only look <DEPTH_LIMIT> moves(cycles) ahead
		while depth < DEPTH_LIMIT:
			# Possible states are held in a buffer
			# Buffer added to board states at the end of the current cycle
			# Avoid endless loop of iterating a constantly incrementing array
			possible_states = []
			# For each of the potential boards
			for board in board_states:
				# A board with all black eliminated has been found
				# Solveable in this cycle, stop generation of more sequences
				if board.black == 0:
					optimal_cycle = True
					possible_states.append(board)
					depth = DEPTH_LIMIT
				elif not optimal_cycle:
					# For each possible move for this board
					# 1. Generate a new board
					# 2. Execute move on new board
					# 3. Add that new board to possible states
					moves = board.available_moves(WHITE)
					for pos_from in moves:
						for pos_to in moves[pos_from]:
							possible_board = copy.deepcopy(board)
							possible_board.move(pos_from, pos_to)
							possible_states.append(possible_board)
			# In the next cycle, generate the boards of the boards we generated
			board_states = possible_states
			depth+= 1

		# Depth limit reached, set the board to the most optimal solution
		# min(black), min(len(moves)) and max(white) or min(-white)
		self = copy.deepcopy(min(board_states, key=lambda board:(
			board.black, 
			len(board.moves), 
			-board.white)))
		return self


# Helper function, return enemy piece type
def opposite(piece):
	if piece == WHITE:
		return BLACK
	elif piece == BLACK:
		return WHITE