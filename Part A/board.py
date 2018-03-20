import copy
import random
from operator import attrgetter

WHITE = "O"
BLACK = "@"
CORNER = "X"
EMPTY = "-"
DEPTH_LIMIT = 4

class Board:
	def __init__(self):
		# 2D Array representation of board state
		self.grid = []
		# Number of white and black pieces on the board in current state
		self.white = 0
		self.black = 0
		# History of moves required to reach current state
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
			# Push row into ith row of grid object
			self.grid.append(row)

	def available_moves(self, player):
		# Available moves are represented by a dict:
		#		 key : valye
		# 	  origin : [north, south, west] 
		# (row, col) : [(row, col), (row, col), (row, col)]
		moves = {}
		# Iterate through each square on the grid, if square == WHITE/BLACK, add list of available moves
		for row in range(len(self.grid)):
			for col in range(len(self.grid[row])):
				if self.grid[row][col] == player:
					#Check available moves for piece at (row,col)
					possible_moves = self.check_moves(row, col)
					moves[(row,col)] = possible_moves
		return moves

	def check_moves(self, row, col):
		moves = []
		# Check north
		try:
			# Check adjacent
			if self.grid[row-1][col] == EMPTY:
				moves.append((row-1,col))
			# Adjacent occupied, check if jump available
			elif self.grid[row-2][col] == EMPTY:
				moves.append((row-2,col))
		except:
			pass
		# Check south
		try:
			if self.grid[row+1][col] == EMPTY:
				moves.append((row+1,col))
			elif self.grid[row+2][col] == EMPTY:
				moves.append((row+2,col))
		except:
			pass
		# Check west
		try:
			if self.grid[row][col-1] == EMPTY:
				moves.append((row,col-1))
			elif self.grid[row][col-2] == EMPTY:
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
		# Randomize order of moves so that, should no solution be found, no bias towards a single direction
		random.shuffle(moves)
		return moves

	def check_eliminated(self, row, col):
		# Determine color of piece we're checking to eliminate and it's opposite
		piece = self.grid[row][col]
		enemy = opposite(piece)

		# Check vertical and horizontal axis, if piece is cornered return true
		# Use try blocks for each axis to catch index out of bounds errors on grid
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
		# Piece not cornered
		return False

	def move(self, pos_from, pos_to):
		# Determine type of piece to move, replace destination with piece and empty origin
		piece = self.grid[pos_from[0]][pos_from[1]]
		self.grid[pos_to[0]][pos_to[1]] = piece
		self.grid[pos_from[0]][pos_from[1]] = EMPTY
		# Add to history of moves for this board
		self.moves.append((pos_from, pos_to))
		# Refresh board, eliminating enemy pieces
		self.refresh(opposite(piece))
		# Refresh board, check for sucides (Elimination priority to player that moved)
		self.refresh(piece)

	def refresh(self, piece):
		# Scan board for pieces that should be eliminated in current state
		for row in range(len(self.grid)):
			for col in range(len(self.grid)):
				if self.grid[row][col] == piece:
					if self.check_eliminated(row, col):
						# Piece eliminated, empty occupying square and deduct piece type count
						self.grid[row][col] = EMPTY
						if piece == BLACK:
							self.black-= 1
						elif piece == WHITE:
							self.white-= 1

	def massacre(self):
		depth = 0
		optimal_cycle = False
		# Potential boards are held in a list of board objects, load current state to begin
		board_states = []
		board_states.append(self)
		# Limited minmax algorithm, only look <DEPTH_LIMIT> number of moves(cycles) ahead
		while depth < DEPTH_LIMIT:
			# Possible states are held in a buffer, added to the board states at the end of the current cycle
			# Avoid endless loop by iterating through constantly incrementing board_states[]
			possible_states = []
			# For each of the potential boards
			for board in board_states:
				# A board with all black eliminated has been found
				# There is a solution in this cycle, can stop generation of more sequences
				if board.black == 0:
					optimal_cycle = True
					possible_states.append(board)
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
			# In the next cycle, generate the potential boards of all the potential boards we generated
			board_states = possible_states
			depth+= 1

		# Depth limit reached, set the board to the most optimal solution this iteration
		# min(black) and min(len(moves))
		self = copy.deepcopy(min(board_states, key=lambda board:(board.black, len(board.moves))))
		return self


# Helper function, return enemy piece type
def opposite(piece):
	if piece == WHITE:
		return BLACK
	elif piece == BLACK:
		return WHITE