import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 15
CELL_SIZE = WIDTH // 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Fonts
font = pygame.font.Font(None, 74)

# Function to draw the grid
def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)

# Function to draw the X and O on the board
def draw_xo(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                pygame.draw.line(screen, LINE_COLOR, (j * CELL_SIZE, i * CELL_SIZE),
                                 ((j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE), LINE_WIDTH)
                pygame.draw.line(screen, LINE_COLOR, ((j + 1) * CELL_SIZE, i * CELL_SIZE),
                                 (j * CELL_SIZE, (i + 1) * CELL_SIZE), LINE_WIDTH)
            elif board[i][j] == 'O':
                pygame.draw.circle(screen, LINE_COLOR, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 10, LINE_WIDTH)

# Function to check for a winner
def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

# Function to check if the board is full
def is_board_full(board):
    return all(all(cell != ' ' for cell in row) for row in board)

# Function to get the available moves
def available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

# Function to get the best move using the Minimax algorithm
def minimax(board, depth, maximizing_player):
    winner = check_winner(board)
    if winner:
        return 1 if winner == 'X' else -1
    elif is_board_full(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in available_moves(board):
            i, j = move
            board[i][j] = 'X'
            eval = minimax(board, depth + 1, False)
            board[i][j] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in available_moves(board):
            i, j = move
            board[i][j] = 'O'
            eval = minimax(board, depth + 1, True)
            board[i][j] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

# Function to get the best move for the computer
def best_move(board):
    best_val = float('-inf')
    best_move = None
    for move in available_moves(board):
        i, j = move
        board[i][j] = 'X'
        move_val = minimax(board, 0, False)
        board[i][j] = ' '
        if move_val > best_val:
            best_val = move_val
            best_move = (i, j)
    return best_move

# Main game loop
def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    player_turn = random.choice([True, False])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                x, y = event.pos
                row = y // CELL_SIZE
                col = x // CELL_SIZE
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    player_turn = not player_turn

        screen.fill(WHITE)
        draw_grid()
        draw_xo(board)

        winner = check_winner(board)
        if winner:
            pygame.time.wait(1000)
            pygame.quit()
            sys.exit()
        elif is_board_full(board):
            pygame.time.wait(1000)
            pygame.quit()
            sys.exit()

        if not player_turn:
            move = best_move(board)
            board[move[0]][move[1]] = 'X'
            player_turn = not player_turn

        pygame.display.flip()

if __name__ == "__main__":
    main()
