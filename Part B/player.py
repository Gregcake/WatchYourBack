'''
Written by Greg Tan (726323) & Luis Adjero (762095)
COMP30024: Artificial Intelligence
Project Part B: Watch Your Back!
Last Edited 11/04/2018

PLayer Class
'''

class Player:

	'''
	Setup internal representation of player and board class
	Input: Color representation for the game
	Return Value: None
	'''
	def __init__(self, colour):
		self.board = Board(color);

	'''
	Referee calls program to make a move, decide what action to take. Should call update() with action at end to self-update.
	Input: Number of turns that have taken place since start of game
	Return:(x,y) for placement phase / ((from_x,from_y),(to_x,to_y)) for move phase / None
	'''
	def action(self, turns):
		pass

	'''
	Referee tells program opponent move, update board class accordingly
	Input: Either player action ((from_x,from_y),(to_x,to_y)), can be player or opponent
	Return: No return value
	Luis
	'''
	def update(self, action)
		pass