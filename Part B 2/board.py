WHITE = "O"
BLACK = "@"
CORNER = "X"

START = 0
BOARD_SIZE = 8
MOVEMENT = 24
SHRINK_1 = 128
SHRINK_2 = 192

class Board:

	def __init__(self, color):
		self.player = color
		self.enemy = opposite(color)
		self.player_pieces = 0
		self.enemy_pieces = 0
		self.grid = {}
		self.lower_bound = 0
		self.upper_bound = 7
		self.set_corners(START)

	def place(self, color, pos):
		self.grid[pos] = color
		if color == self.player:
			self.player_pieces+= 1
		elif color == self.enemy:
			self.enemy_pieces+= 1
		self.update(color)

	def available_placements(self, color):
		possible = []
		if color == WHITE:
			y_min, y_max = 0,5
		elif color == BLACK:
			y_min, y_max = 2,7

		for y in range(y_min, y_max+1):
			for x in range(BOARD_SIZE):
				if (x,y) not in self.grid:
					possible.append((x,y))
		return possible

	def move(self, color, pos_from, pos_to):
		del self.grid[pos_from]
		self.grid[pos_to] = color
		self.update(color)

	def available_moves(self, color):
		possible = []
		for pos in self.grid:
			if self.grid[pos] == color:
				x = pos[0]
				y = pos[1]
				if (x,y+1) not in self.grid and self.within_bounds((x,y+1)):
					possible.append((pos,(x,y+1)))
				elif (x,y+1) in self.grid and (x,y+2) not in self.grid and self.within_bounds((x,y+2)):
					possible.append((pos,(x,y+2)))
				if (x,y-1) not in self.grid and self.within_bounds((x,y-1)):
					possible.append((pos,(x,y-1)))
				elif (x,y-1) in self.grid and (x,y-2) not in self.grid and self.within_bounds((x,y-2)):
					possible.append((pos,(x,y-2)))
				if (x+1,y) not in self.grid and self.within_bounds((x+1,y)):
					possible.append((pos,(x+1,y)))
				elif (x+1,y) in self.grid and (x+2,y) not in self.grid and self.within_bounds((x+2,y)):
					possible.append((pos,(x+2,y)))
				if (x-1,y) not in self.grid and self.within_bounds((x-1,y)):
					possible.append((pos,(x-1,y)))
				elif (x-1,y) in self.grid and (x-2,y) not in self.grid and self.within_bounds((x-2,y)):
					possible.append((pos,(x-2,y)))
		return possible


	def update(self, color):
		remove = []
		for pos in self.grid:
			if self.grid[pos] == opposite(color) and self.check_eliminated(pos):
				remove.append(pos)
		for pos in remove:
			del self.grid[pos]
			if opposite(color) == self.player:
				self.player_pieces-= 1
			elif opposite(color) == self.enemy:
				self.enemy_pieces-= 1

		remove = []
		for pos in self.grid:
			if self.grid[pos] == color and self.check_eliminated(pos):
				remove.append(pos)
		for pos in remove:
			del self.grid[pos]
			if color == self.player:
				self.player_pieces-= 1
			elif color == self.enemy:
				self.enemy_pieces-= 1

	def check_eliminated(self, pos):
		x = pos[0]
		y = pos[1]
		enemy = opposite(self.grid[pos])
		north = self.grid.get((x,y-1))
		south = self.grid.get((x,y+1))
		east = self.grid.get((x+1,y))
		west = self.grid.get((x-1,y))
		if ((north==enemy or north==CORNER) and (south==enemy or south==CORNER)):
			return True
		elif ((east==enemy or east==CORNER) and (west==enemy or west==CORNER)):
			return True
		else:
			return False

	def apply_shrink(self, turn):
		if turn == SHRINK_1+MOVEMENT:
			self.lower_bound = 1
			self.upper_bound = 6
		elif turn == SHRINK_2+MOVEMENT:
			self.lower_bound = 2
			self.upper_bound = 5

		remove = []
		for pos in self.grid:
			if not self.within_bounds(pos):
				remove.append(pos)
		for pos in remove:
			del self.grid[pos]
		self.set_corners(turn)


	def set_corners(self, turn):
		if turn == START:
			self.grid[(0,0)] = CORNER
			self.grid[(0,7)] = CORNER
			self.grid[(7,7)] = CORNER
			self.grid[(7,0)] = CORNER
		elif turn == SHRINK_1+MOVEMENT:
			self.grid[(1,1)] = CORNER
			self.grid[(1,6)] = CORNER
			self.grid[(6,6)] = CORNER
			self.grid[(6,1)] = CORNER
		elif turn == SHRINK_2+MOVEMENT:
			self.grid[(2,2)] = CORNER
			self.grid[(2,5)] = CORNER
			self.grid[(5,5)] = CORNER
			self.grid[(5,2)] = CORNER

	def within_bounds(self, pos):
		if pos[0]<self.lower_bound or pos[0]>self.upper_bound or pos[1]<self.lower_bound or pos[1]>self.upper_bound:
			return False
		else:
			return True

# Helper function, return enemy piece type
def opposite(piece):
	if piece == WHITE:
		return BLACK
	elif piece == BLACK:
		return WHITE

def print_board(board):
	print("")
	for row in range(8):
		line = ""
		for col in range(8):
			line+=board.grid.get((col,row), " ")
			line+=" "
		print(line)
	print(board.player_pieces)
	print(board.enemy_pieces)
	print("================")

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