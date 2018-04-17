'''
Written by Greg Tan (726323) & Luis Adjero (762095)
COMP30024: Artificial Intelligence
Project Part B: Watch Your Back!
Last Edited 11/04/2018

Board Class
'''

WHITE = "O"
BLACK = "@"
CORNER = "X"
EMPTY = "-"

INIT_SIZE = 8

class Board:
	def __init__(self, player):
		self.grid = empty_grid(INIT_SIZE)
		apply_corners(self)
		self.black = 0
		self.white = 0
		self.player = player
		self.enemy = opposite(player)

	# Returns a list of available moves for each piece on the board the player controls
	# [((from_x,from_y),(to_x,to_y)), ((from_x,from_y),(to_x,to_y))]
	def available_moves(self):
		moves = []
		for y in range(len(self.grid)):
			for x in range(len(self.grid)):
				if self.grid[y][x] == self.player:
					for move in check_moves((x,y)):
						moves.append(move)
		return moves

	# Returns a list of potential moves the player can make that will result in a kill
	# [((from_x,from_y),(to_x,to_y)), ((from_x,from_y),(to_x,to_y))]
	# Luis
	def potential_kills(self):
		pass

	# Returns a list of pieces the player controls that are in danger of elimination
	# [(x,y), (x,y)]
	# Luis
	def potential_deaths(self):
		pass

	# Returns a list of moves that a piece at position can make
	# Position = (x,y)
	# [((x,y),(to_x,to_y)), ((x,y),(to_x,to_y))]
	def check_moves(self, position):
		moves = []
		x = position[0]
		y = position[1]

		# Check north
		try:
			# Check adjacent, block negative indexing
			if self.grid[y-1][x] == EMPTY and y-1>=0:
				moves.append((y-1,x))
			# Check if jump available, block negative indexing
			elif self.grid[y-2][x] == EMPTY and y-2>=0:
				moves.append((y-2,x))
		except:
			pass
		# Check south
		try:
			# Check adjacent, catch index out of bounds errors
			if self.grid[y+1][x] == EMPTY:
				moves.append((y+1,x))
			elif self.grid[y+2][x] == EMPTY:
				moves.append((y+2,x))
		except:
			pass
		# Check west
		try:
			if self.grid[y][x-1] == EMPTY and x-1>=0:
				moves.append((y,x-1))
			elif self.grid[y][x-2] == EMPTY and x-2>=0:
				moves.append((y,x-2))
		except:
			pass
		# Check east
		try:
			if self.grid[y][x+1] == EMPTY:
				moves.append((y,x+1))
			elif self.grid[y][x+2] == EMPTY:
				moves.append((y,x+2))
		except:
			pass
		# Randomize order of moves
		# Should no solution be found, no bias towards a single direction
		random.shuffle(moves)
		return moves


	# Apply a move to the board and refresh board
	# Color = color of piece that is being moved
	# Position = [((from_x,from_y),(to_x,to_y))]
	def move(self, color, position):
		from_x = position[0][0]
		from_y = position[0][1]
		to_x = position[1][0]
		to_y = position[1][1]
		self.grid[from_y][from_x] = EMPTY
		self.grid[to_y][to_x] = color
		refresh(color)

	# Check eliminations of opposite(color), check eliminations of color
	def refresh(self, color):
		order = [opposite(color), color]
		for piece in order:
			for y in range(len(self.grid)):
				for x in range(len(self.grid)):
					if self.grid[y][x] == piece:
						if self.check_eliminated((x,y)):
							# Piece eliminated
							# Empty occupying square and deduct piece type count
							self.grid[y][x] = EMPTY
							if piece == BLACK:
								self.black-= 1
							elif piece == WHITE:
								self.white-= 1

	# Given a row,col, check if the piece on that square is eliminated
	# True if eliminated, false otherwise
	def check_eliminated(self, position):
		# Determine color of piece we're checking to eliminate and it's opposite
		x = position[0]
		y = position[1]
		piece = self.grid[y][x]
		enemy = opposite(piece)

		# Check vertical and horizontal axis, if piece is cornered return true
		# Use try blocks for each axis to catch index OOB errors on grid
		try:
			north = self.grid[y-1][x]
			south = self.grid[y+1][x]
			if((north == enemy or north == CORNER) and
				(south == enemy or south == CORNER)):
				return True
		except:
			pass
		try:
			east = self.grid[y][x-1]
			west = self.grid[y][x+1]
			if((east == enemy or east == CORNER) and 
				(west == enemy or west == CORNER)):
				return True
		except:
			pass
		# Piece not cornered
		return False

	# Shrink board, refresh board
	def process_shrink(self, color):
		apply_shrink()
		apply_corners()
		refresh(self.player)

	# Apply shrinkage on board
	def apply_shrink(self):
		del self.grid[0]
		del self.grid[-1]
		for row in self.grid:
			del row[0]
			del row[-1]

	def apply_corners(self):
		self.grid[0][-1] = CORNER
		self.grid[0][0] = CORNER
		self.grid[-1][0] = CORNER
		self.grid[-1][-1] = CORNER

# Helper function, return enemy piece type
def opposite(piece):
	if piece == WHITE:
		return BLACK
	elif piece == BLACK:
		return WHITE

def empty_grid(size):
	grid = [[EMPTY for i in range(size)] for i in range(size)]
	return grid