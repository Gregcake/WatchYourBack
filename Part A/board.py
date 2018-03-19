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
					possible_moves = checkmoves(self.grid, row, col)
					moves[(row,col)] = possible_moves
		return moves

	def copy_board(self, board):
		self.grid = board.grid
		self.white = board.white
		self.black = board.black
		self.moves = board.moves

	def move(self, pos_from, pos_to, player, enemy):
		new_board = Board()
		new_board.copy_board(self)
		new_board.grid[pos_from[0]][pos_from[1]] == EMPTY
		new_board.grid[pos_to[0]][pos_to[1]] == player
		new_board.moves.append((pos_from,pos_to))
		new_board.refresh(enemy)
		return new_board

	def refresh(self, enemy):
		for row in range(len(self.grid)):
			for col in range(len(self.grid)):
				if self.grid[row][col] == enemy:
					try:
						vertical = checkelimination(self.grid[row-1][col], self.grid[row+1][col], enemy)
					except:
						pass
					try:
						horizontal = checkelimination(self.grid[row][col-1], self.grid[row][col+1], enemy)
					except:
						pass
					if vertical or horizontal:
						self.grid[row][col] == EMPTY
						if enemy == BLACK:
							self.black-= 1
						elif enemy == WHITE:
							self.white-= 1

def checkelimination(axis_1, axis_2, enemy):
	if(axis_1 == enemy or CORNER) and (axis_2 == enemy or CORNER):
		return True
	else:
		return False




def checkmoves(grid, row, col):
		moves = []
		#Check north
		try:
			#Check adjacent
			if grid[row-1][col] == EMPTY:
				moves.append((row-1,col))
			#Adjacent occupied, check if jump available
			elif grid[row-2][col] == EMPTY:
				moves.append((row-2,col))
		except:
			pass
		#Check south
		try:
			if grid[row+1][col] == EMPTY:
				moves.append((row+1,col))
			elif grid[row+2][col] == EMPTY:
				moves.append((row+2,col))
		except:
			pass
		#Check west
		try:
			if grid[row][col-1] == EMPTY:
				moves.append((row,col-1))
			elif grid[row][col-2] == EMPTY:
				moves.append((row,col-2))
		except:
			pass
		#Check east
		try:
			if grid[row][col+1] == EMPTY:
				moves.append((row,col+1))
			elif grid[row][col+2] == EMPTY:
				moves.append((row,col+2))
		except:
			pass
		return moves