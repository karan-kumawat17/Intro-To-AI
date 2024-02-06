import random

def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

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

def is_board_full(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

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

def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    player_turn = random.choice([True, False])

    while True:
        print_board(board)

        if player_turn:
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
            if board[row][col] == ' ':
                board[row][col] = 'O'
                player_turn = not player_turn
            else:
                print("Cell already occupied. Try again.")
                continue
        else:
            print("Computer's turn:")
            move = best_move(board)
            board[move[0]][move[1]] = 'X'
            player_turn = not player_turn

        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"{winner} wins!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break

if __name__ == "__main__":
    main()
