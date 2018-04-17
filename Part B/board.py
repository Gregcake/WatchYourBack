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
        all_kills = []
        for col in range(len(self.grid)):
            for row in range(len(col)):
                if self.grid[col][row] == self.player:
                    #get a list of all moves that piece can make
                    piece_moves = self.check_moves(row, col)
                    # (col1,row1) refers to the piece's position
                    for ((col1,row1),(col2,row2)) in piece_moves:
                        elim = self.check_eliminated(row2,col2,self.player,self.enemy)
                        if elim:
                            all_kills.append(((col1,row1), (col2,row2)))
        return all_kills
                        

    # Returns a list of pieces the player controls that are in danger of elimination
    # [(x,y), (x,y)]
    def potential_deaths(self):
        endangered = []
        for col in range(len(self.grid)):
            for row in range(len(col)):
                if self.grid[col][row] == self.player:
                    elim = self.check_eliminated(row,col,self.enemy,self.player)
                    if elim:
                        endangered.append((col,row))
        pass

    # Returns a list of moves that a piece at position can make
    # Position = (x,y)
    # [((x,y),(to_x,to_y)), ((x,y),(to_x,to_y))]
    """
    def check_moves(self, position): 
        pass
    """
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
        return
    # Given a row,col, check if the piece on that square is eliminated
    # True if eliminated, false otherwise
    def check_eliminated(self, row, col, piece, enemy):
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
        

# Helper function, return enemy piece type
def opposite(piece):
    if piece == WHITE:
        return BLACK
    elif piece == BLACK:
        return WHITE

def empty_grid(size):
    grid = [[EMPTY for i in range(size)] for i in range(size)]
    return grid
