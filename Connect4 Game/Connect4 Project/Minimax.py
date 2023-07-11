import numpy as np
import random
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

Agent = 0
Computer = 1

EMPTY = 0
Agent_PIECE = 1
Computer_PIECE = 2

WINDOW_LENGTH = 4

def start_game_minimax(d):

	def create_board():
		board = np.zeros((ROW_COUNT, COLUMN_COUNT))
		return board

	def drop_piece(board, row, col, piece):
		board[row][col] = piece

	def is_valid_location(board, col):
		return board[ROW_COUNT - 1][col] == 0

	def get_next_open_row(board, col):
		for r in range(ROW_COUNT):
			if board[r][col] == 0:
				return r

	def print_board(board):
		print(np.flip(board, 0))

	def winning_move(board, piece):
		# Check horizontal locations for win
		for c in range(COLUMN_COUNT - 3):
			for r in range(ROW_COUNT):
				if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
					c + 3] == piece:
					return True

		# Check vertical locations for win
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT - 3):
				if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
					c] == piece:
					return True

		# Check positively sloped diaganols
		for c in range(COLUMN_COUNT - 3):
			for r in range(ROW_COUNT - 3):
				if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
						board[r + 3][c + 3] == piece:
					return True

		# Check negatively sloped diaganols
		for c in range(COLUMN_COUNT - 3):
			for r in range(3, ROW_COUNT):
				if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
						board[r - 3][c + 3] == piece:
					return True

	def evaluate_window(window, piece):
		score = 0
		opp_piece = Agent_PIECE
		if piece == Agent_PIECE:
			opp_piece = Computer_PIECE

		if window.count(piece) == 4:
			score += 100
		elif window.count(piece) == 3 and window.count(EMPTY) == 1:
			score += 5
		elif window.count(piece) == 2 and window.count(EMPTY) == 2:
			score += 2

		if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
			score -= 4

		return score

	def score_position(board, piece):
		score = 0

		## Score center column
		center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
		center_count = center_array.count(piece)
		score += center_count * 3

		## Score Horizontal
		for r in range(ROW_COUNT):
			row_array = [int(i) for i in list(board[r, :])]
			for c in range(COLUMN_COUNT - 3):
				window = row_array[c:c + WINDOW_LENGTH]
				score += evaluate_window(window, piece)

		## Score Vertical
		for c in range(COLUMN_COUNT):
			col_array = [int(i) for i in list(board[:, c])]
			for r in range(ROW_COUNT - 3):
				window = col_array[r:r + WINDOW_LENGTH]
				score += evaluate_window(window, piece)

		## Score posiive sloped diagonal
		for r in range(ROW_COUNT - 3):
			for c in range(COLUMN_COUNT - 3):
				window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
				score += evaluate_window(window, piece)

		for r in range(ROW_COUNT - 3):
			for c in range(COLUMN_COUNT - 3):
				window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
				score += evaluate_window(window, piece)

		return score

	def is_terminal_node(board):
		return winning_move(board, Agent_PIECE) or winning_move(board, Computer_PIECE) or len(
			get_valid_locations(board)) == 0

	def minimax(board, depth, maximizingPlayer):
		valid_locations = get_valid_locations(board)
		is_terminal = is_terminal_node(board)
		if depth == 0 or is_terminal:
			if is_terminal:
				if winning_move(board, Computer_PIECE):
					return (None, 100000000000000)
				elif winning_move(board, Agent_PIECE):
					return (None, -10000000000000)
				else:  # Game is over, no more valid moves
					return (None, 0)
			else:  # Depth is zero
				return (None, score_position(board, Computer_PIECE))
		if maximizingPlayer:
			value = -math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = get_next_open_row(board, col)
				if row is None:
					continue
				b_copy = board.copy()
				drop_piece(b_copy, row, col, Computer_PIECE)
				new_score = minimax(b_copy, depth - 1, False)[1]
				if new_score > value:
					value = new_score
					column = col
			return column, value
		else:  # Minimizing player
			value = math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = get_next_open_row(board, col)
				if row is None:
					continue
				b_copy = board.copy()
				drop_piece(b_copy, row, col, Agent_PIECE)
				new_score = minimax(b_copy, depth - 1, True)[1]
				if new_score < value:
					value = new_score
					column = col
			return column, value

	def get_valid_locations(board):
		valid_locations = []
		for col in range(COLUMN_COUNT):
			if is_valid_location(board, col):
				valid_locations.append(col)
		return valid_locations

	def pick_best_move(board, piece):

		valid_locations = get_valid_locations(board)
		best_score = -10000
		best_col = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			temp_board = board.copy()
			drop_piece(temp_board, row, col, piece)
			score = score_position(temp_board, piece)
			if score > best_score:
				best_score = score
				best_col = col

		return best_col

	def draw_board(board):
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT):
				pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
				pygame.draw.circle(screen, BLACK, (
				int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT):
				if board[r][c] == Agent_PIECE:
					pygame.draw.circle(screen, RED, (
					int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
				elif board[r][c] == Computer_PIECE:
					pygame.draw.circle(screen, YELLOW, (
					int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
		pygame.display.update()

	board = create_board()
	print_board(board)
	game_over = False

	pygame.init()

	SQUARESIZE = 100

	width = COLUMN_COUNT * SQUARESIZE
	height = (ROW_COUNT + 1) * SQUARESIZE

	size = (width, height)

	RADIUS = int(SQUARESIZE / 2 - 5)

	screen = pygame.display.set_mode(size)
	draw_board(board)
	pygame.display.update()

	myfont = pygame.font.SysFont("monospace", 75)

	turn = random.randint(Agent, Computer)

	while not game_over:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			# Ask for Player 1 Input
			if turn == Agent:
				col, minimax_score = minimax(board, d, False)

				if is_valid_location(board, col):
					# pygame.time.wait(600)
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, Agent_PIECE)

					if winning_move(board, Agent_PIECE):
						label = myfont.render("Agent wins!!", 1, RED)
						screen.blit(label, (40, 10))
						game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)

			# Ask for Player 2 Input
			if turn == Computer and not game_over:
				col, minimax_score = minimax(board, d, False)

				if is_valid_location(board, col):
					# pygame.time.wait(600)
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, Computer_PIECE)

					if winning_move(board, Computer_PIECE):
						label = myfont.render("Computer wins!!", 1, YELLOW)
						screen.blit(label, (40, 10))
						game_over = True

					print_board(board)
					draw_board(board)

					turn += 1
					turn = turn % 2

		if game_over:
			pygame.time.wait(3000)

if __name__ == "__main__":
    start_game_minimax()