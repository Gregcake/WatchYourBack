'''
Written by Greg Tan (726323) & Luis Adjero (762095)
COMP30024: Artificial Intelligence
Project Part B: Watch Your Back!
Last Edited 11/04/2018
Board Class
'''
WHITE_S = "white"
BLACK_S = "black"
WHITE = "O"
BLACK = "@"
CORNER = "X"
EMPTY = "-"

INIT_SIZE = 8
import random
class Board:

    def __init__(self, color):
        if color == WHITE_S:
            color = WHITE
        elif color == BLACK_S:
            color = BLACK
        self.player = color
        self.enemy = opposite(color)
        self.player_pieces = 0
        self.enemy_pieces = 0
        self.grid = empty_grid(INIT_SIZE)
        self.apply_corners()

    def place(self, color, pos):
        x = pos[0]
        y = pos[1]
        self.grid[y][x] = color
        self.update(color)

    def available_placements(self, color):
        possible = []
        if color == WHITE:
            y_min, y_max = 0,5
        else:
            y_min, y_max = 2,7

        for y in range(y_min, y_max+1):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == EMPTY:
                    possible.append((x,y))
        return possible

    def available_moves(self, color):
        possible = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                piece = self.grid[y][x]
                if piece == color:
                    for move in self.check_moves((x,y)):
                        possible.append(((x,y),move))
        return possible

    def check_moves(self,pos):
        x = pos[0]
        y = pos[1]
        moves = []
        # Check north
        try:
            # Check adjacent, block negative indexing
            if self.grid[y-1][x] == EMPTY and y-1>=0:
                moves.append((x,y-1))
            # Check if jump available, block negative indexing
            elif self.grid[y-2][x] == EMPTY and y-2>=0:
                moves.append((x,y-2))
        except:
            pass
        # Check south
        try:
            # Check adjacent, catch index out of bounds errors
            if self.grid[y+1][x] == EMPTY:
                moves.append((x,y+1))
            elif self.grid[y+2][x] == EMPTY:
                moves.append((x,y+2))
        except:
            pass
        # Check west
        try:
            if self.grid[y][x-1] == EMPTY and x-1>=0:
                moves.append((x-1,y))
            elif self.grid[y][x-2] == EMPTY and x-2>=0:
                moves.append((x-2,y))
        except:
            pass
        # Check east
        try:
            if self.grid[y][x+1] == EMPTY:
                moves.append((x+1,y))
            elif self.grid[y][x+2] == EMPTY:
                moves.append((x+2,y))
        except:
            pass
        # Randomize order of moves
        # Should no solution be found, no bias towards a single direction
        random.shuffle(moves)
        return moves

    def move(self, color, pos_from, pos_to):
        x_from = pos_from[0]
        y_from = pos_from[1]
        x_to = pos_to[0]
        y_to = pos_to[1]
        self.grid[y_from][x_from] = EMPTY
        self.grid[y_to][x_to] = color
        self.update(color)

    def update(self, color):
        self.process_eliminations(color)
        self.process_eliminations(opposite(color))
        player = 0
        enemy = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                piece = self.grid[y][x]
                if piece == self.player:
                    player+= 1
                elif piece == self.enemy:
                    enemy+= 1
        self.player_pieces = player
        self.enemy_pieces = enemy

    def process_eliminations(self, color):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                piece = self.grid[y][x]
                if piece == opposite(color) and self.check_eliminations((x,y)):
                    self.grid[y][x] = EMPTY

    def check_eliminations(self, pos):
        x = pos[0]
        y = pos[1]
        piece = self.grid[y][x]
        enemy = opposite(piece)

        # Check vertical and horizontal axis, if piece is cornered return true
        # Use try blocks for each axis to catch index OOB errors on grid
        try:
            north = self.grid[y-1][x]
            south = self.grid[y+1][x]
            if((north == enemy or north == CORNER) and (south == enemy or south == CORNER)):
                return True
        except:
            pass
        try:
            east = self.grid[y][x-1]
            west = self.grid[y][x+1]
            if((east == enemy or east == CORNER) and (west == enemy or west == CORNER)):
                return True
        except:
            pass
        # Piece not cornered
        return False

    def apply_shrink(self):
        del(self.grid[0])
        del(self.grid[-1])
        for row in self.grid:
            del(row[0])
            del(row[-1])
        self.apply_corners()
        
    def apply_corners(self):
        self.grid[0][0] = CORNER
        self.grid[0][-1] = CORNER
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

def print_board(board):
    for row in board.grid:
        print(row)

board = Board("white")
print_board(board)
print(board.player_pieces)
print(board.enemy_pieces)
print("")
