from board import Board
BOARD_SIZE = 8
MOVES = "Moves"
MASSACRE = "Massacre"
WHITE = "O"
BLACK = "@"
EMPTY = "-"
MAX_DEPTH = 4

def main():
	board = Board()
	board.read_from_stdin(BOARD_SIZE)
	task = input()
	if task == MOVES:
		print(sum(len(x) for x in board.available_moves(WHITE).values()))
		print(sum(len(x) for x in board.available_moves(BLACK).values()))
	elif task == MASSACRE:
		while board.black>0:
			possible_scenarios = []
			possible_scenarios.append(board)
			depth = 0
			while depth < MAX_DEPTH:
				next_set = []
				for scenario in possible_scenarios:
					possible_moves = scenario.available_moves(WHITE)
					for pos_from in possible_moves:
						for pos_to in possible_moves[pos_from]:
							next_set.append(scenario.move(pos_from,pos_to,WHITE,BLACK))
				possible_scenarios = []
				possible_scenarios.extend(next_set)
				depth+= 1
			min_black = board.black
			min_moves = len(board.moves)
			for scenario in possible_scenarios:
				if scenario.black<=min_black or scenario.black == 0:
					if len(scenario.moves) <= min_moves:
						board = scenario
		print(board.grid)
		print(board.black)
		print(board.white)

#Driver execution
if __name__ == '__main__':
	main()