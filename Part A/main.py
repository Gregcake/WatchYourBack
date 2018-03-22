from board import Board
import copy
import time #TODO: Remove

BOARD_SIZE = 8
MOVES = "Moves"
MASSACRE = "Massacre"
WHITE = "O"
BLACK = "@"
EMPTY = "-"

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
	print("Runtime: %s seconds" % (time.time() - start_time))