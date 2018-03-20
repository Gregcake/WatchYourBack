from board import Board
import copy

BOARD_SIZE = 8
MOVES = "Moves"
MASSACRE = "Massacre"
WHITE = "O"
BLACK = "@"
EMPTY = "-"

def main():
	board = Board()
	board.read_from_stdin(BOARD_SIZE)
	task = input()
	if task == MOVES:
		print(sum(len(x) for x in board.available_moves(WHITE).values()))
		print(sum(len(x) for x in board.available_moves(BLACK).values()))
	elif task == MASSACRE:
		optimal = copy.deepcopy(board)
		while(board.black>0):
			board = board.massacre()
		'''for move in board.moves:
			print(move)
			optimal.move(move[0],move[1])
			for row in optimal.grid:
				print(row)
			print("\n")'''

#Driver execution
if __name__ == '__main__':
	main()