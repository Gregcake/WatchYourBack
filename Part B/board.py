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
import random
class Board:

    def __init__(self, player):
        if player == 'white':
            pieceColor = WHITE
        else:
            pieceColor = BLACK
        self.grid = empty_grid(INIT_SIZE)
        self.apply_corners()
        self.black = 0
        self.white = 0
        self.player = pieceColor
        self.enemy = opposite(pieceColor)
        self.turns = 0

    # Returns a list of available moves for each piece on the board the player controls
    # [((from_x,from_y),(to_x,to_y)), ((from_x,from_y),(to_x,to_y))]
    def available_moves(self):
        moves = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.grid[y][x] == self.player:
                    for move in self.check_moves((x,y)):
                        ''' changed from append(move) to append(piece,move)'''
                        piece = (x,y)
                        moves.append((piece, move))
        return moves

    # Returns a list of potential moves the player can make that will result in a kill
  # [((from_x,from_y),(to_x,to_y)), ((from_x,from_y),(to_x,to_y))]
    def potential_kills(self):
        all_kills = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.grid[y][x] == self.player:
                    #get a list of all moves that piece can make
                    piece_moves = self.check_moves((x, y))
                    # (col1,row1) refers to the piece's position
                    for ((col1,row1),(col2,row2)) in piece_moves:
                        elim = self.check_eliminated((x,y))
                        if elim:
                            all_kills.append(((col1,row1), (col2,row2)))
        return all_kills

    # Returns a list of pieces the player controls that are in danger of elimination
    # [(x,y), (x,y)]
    def potential_deaths(self):
        endangered = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.grid[y][x] == self.player:
                    elim = self.check_eliminated((x,y))
                    if elim:
                        endangered.append((x,y))
        return endangered

    # Returns a list of moves that a piece at position can make
    # Position = (x,y)
    # [((x,y),(to_x,to_y)), ((x,y),(to_x,to_y))]
    '''previously moves.append((y_ord,x_ord)) but now moves.append((x_ord,y_ord))
    [y][x] when indexing, (x,y) when representing board position
    '''
    def check_moves(self, position):
        moves = []
        x = position[0]
        y = position[1]

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
        self.refresh(color)

    def check_place(self, color, position):
        x = position[0]
        y = position[1]

        if (self.grid[y][x] == EMPTY):
            return True
        else:
            return False

    def place(self, color, position):
        if position == None:
            return
        
        x = position[0]
        y = position[1]
        self.grid[y][x] = color
        if color == WHITE:
            self.white+= 1
        else:
            self.black+= 1

        
        self.refresh(color)
        return

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
                print("elimination north-south at: "+str(position))
                return True
        except:
            pass
        try:
            east = self.grid[y][x-1]
            west = self.grid[y][x+1]
            if((east == enemy or east == CORNER) and 
                (west == enemy or west == CORNER)):
                
                print("elimination east-west at: "+str(position))
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

    def print_board(self):
        print("\n===")
        print(str(self.player)+"'s board")
        for row in range(INIT_SIZE):
            print(self.grid[row])
        print("===")
        

# Helper function, return enemy piece type
def opposite(piece):
    if piece == WHITE:
        return BLACK
    elif piece == BLACK:
        return WHITE

def empty_grid(size):
    grid = [[EMPTY for i in range(size)] for i in range(size)]
    return grid
