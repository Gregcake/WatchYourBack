'''
Written by Greg Tan (726323) & Luis Adjero (762095)
COMP30024: Artificial Intelligence
Project Part B: Watch Your Back!
Last Edited 11/04/2018

PLayer Class
'''
import time
from board import Board
from strategy import Strategy

MOVEMENT = 24
SHRINK_1 = 128
SHRINK_2 = 192

class Player:
    '''
    Setup internal representation of player and board class
    Input: Color representation for the game
    Return: None
    '''
    def __init__(self, color):
        self.board = Board(color)
        self.strategy = Strategy()
        self.player = self.board.player
        self.enemy = self.board.enemy
        self.turns = 0
        self.isMovement = False

    '''
    Referee calls program to make a move, decide what action to take. Should call update() with action at end to self-update.
    Input: Number of turns that have taken place since start of phase
    Return:(x,y) for placement phase / ((from_x,from_y),(to_x,to_y)) for move phase / None
    '''
    def action(self, turns):
        t = time.time()
        if self.turns < 24:
            action = self.strategy.placement(self.board, self.player)
        else:
            action = self.strategy.movement(self.board, self.player)
        self.update(action, self.player)
        return action
            
    '''
    Referee tells program opponent move, update board class accordingly
    Input: Either player action ((from_x,from_y),(to_x,to_y)), can be player or opponent
    Return: None
    '''
    def update(self, action, color = None):
        if color == None:
            color = self.enemy

        if self.turns < 24:
            self.board.place(color,action)
        else:
            pos_from = action[0]
            pos_to = action[1]
            self.board.move(color, pos_from, pos_to)

        self.turns+= 1
        if self.turns == SHRINK_1+MOVEMENT or self.turns == SHRINK_2+MOVEMENT:
            self.board.apply_shrink()
            self.board.update(color)


def print_board(board):
    for row in board.grid:
        string = ""
        for col in row:
            if col != "?":
                string+= col
            else:
                string+= " "
            string+= " "
        print(string)