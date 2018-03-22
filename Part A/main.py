'''
Written by Greg Tan (726323) & Luis Adjero (762095)
COMP30024: Artificial Intelligence
Project Part A: Massacre
Last Edited 22/03/2018

Driver Program
'''

from board import Board
import copy
import time

BOARD_SIZE = 8
MOVES = "Moves"
MASSACRE = "Massacre"
WHITE = "O"
BLACK = "@"
DEBUG = 1 # Set to 0 to output runtime


def main():
	# Initalize start state from stdin
	board = Board()
	board.read_from_stdin(BOARD_SIZE)

	# Determine move or massacre
	task = input()
	
	if task == MOVES:
		# Print sum of all available moves for every white piece
		print(sum(len(x) for x in board.available_moves(WHITE).values()))
		# Print sum of all available moves for every black piece
		print(sum(len(x) for x in board.available_moves(BLACK).values()))
	elif task == MASSACRE:
		# MinMax Limited Search (Depth factor of 4)
		# Keep running while black pieces still exists on the board
		while(board.black>0):
			board = board.massacre()

		# Output sequence of moves to achieve massacre
		for pos_from, pos_to in board.moves:
			print(str(pos_from[::-1]) + " -> " + str(pos_to[::-1]))

#Driver execution
if __name__ == '__main__':
	start_time = time.time()
	main()
	if DEBUG == 0: 
		print("Runtime: %s seconds" % (time.time() - start_time))

#Algorithmsarefun