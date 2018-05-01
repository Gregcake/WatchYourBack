'''
Written by Greg Tan (726323) & Luis Adjero (762095)
COMP30024: Artificial Intelligence
Project Part B: Watch Your Back!
Last Edited 11/04/2018

PLayer Class
'''
PLACEMENT = 1
MOVE = 2

class Player:
    '''
    Setup internal representation of player and board class
    Input: Color representation for the game
    Return Value: None
    '''
    def __init__(self, color):
        self.board = Board(color)
        self.player = self.board.player
        self.enemy = self.board.enemy

    '''
    Referee calls program to make a move, decide what action to take. Should call update() with action at end to self-update.
    Input: Number of turns that have taken place since start of game
    Return:(x,y) for placement phase / ((from_x,from_y),(to_x,to_y)) for move phase / None
    '''
    def action(self, turns):
        #update board to represent enemy move
        update(action, self.enemy)
        # placementt phase
        if (turns < 24):
            my_move = random.shuffle(self.board.available_moves())[0]
            return my_move
        # movement phase
        else:
            my_move = random.shuffle(self.board.available_moves())[0]
            return my_move
      
    '''
    Referee tells program opponent move, update board class accordingly
    Input: Either player action ((from_x,from_y),(to_x,to_y)), can be player or opponent
    Return: No return value
    '''
    def update(self, action, color):
      if len(action[0]) == PLACEMENT:
        self.board.place(color, action)
      elif len(action[0]) == MOVE:
        self.board.move(color, action)

