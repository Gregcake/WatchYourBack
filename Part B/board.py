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
		pass

	# Returns a list of potential moves the player can make that will result in a kill
	# [((from_x,from_y),(to_x,to_y)), ((from_x,from_y),(to_x,to_y))]
	def potential_kills(self):
		pass

	# Returns a list of pieces the player controls that are in danger of elimination
	# [(x,y), (x,y)]
	def potential_deaths(self):
		pass

	# Returns a list of moves that a piece at position can make
	# Position = (x,y)
	# [((x,y),(to_x,to_y)), ((x,y),(to_x,to_y))]
	def check_moves(self, position):
		pass

	# Apply a move to the board and refresh board
	# Color = color of piece that is being moved
	# Position =  [((from_x,from_y),(to_x,to_y)), ((from_x,from_y),(to_x,to_y))]
	def move(self, color, position):
		pass

	# Check eliminations of opposite(color), check eliminations of color
	def refresh(self, color):
		pass

	# Apply elimination onto board
	def process_eliminations(self, color):
		pass

	# Shrink board, refresh board
	def process_shrink(self, color):
		pass

	# Apply shrinkage on board
	def apply_shrink(self):
		pass

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