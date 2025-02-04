import logging
from copy import deepcopy

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def utility_function(piece_min, piece_max, board):
    if wins(piece_min, board):
        return -1
    if wins(piece_max, board):
        return 1
    if is_full(board):
        return 0
    return None

def is_full(board):
    return all(cell != '_' for row in board for cell in row)

def wins(piece, board):
    return any(
        all(board[r][c] == piece for c in range(3)) or
        all(board[c][r] == piece for c in range(3)) for r in range(3)
    ) or (
        board[0][0] == board[1][1] == board[2][2] == piece or
        board[0][2] == board[1][1] == board[2][0] == piece
    )

def generate_moves(piece, board):
    moves = []
    for r in range(3):
        for c in range(3):
            if board[r][c] == '_':
                new_board = deepcopy(board)
                new_board[r][c] = piece
                moves.append(new_board)
    return moves

def minimax(turn, piece_min, piece_max, board, alpha=float('-inf'), beta=float('inf')):
    logging.debug(f"Minimax called for turn: {turn}\n{board}")

    if wins(piece_min, board) or wins(piece_max, board) or is_full(board):
        utility = utility_function(piece_min, piece_max, board)
        logging.info(f"Utility value: {utility}")
        return utility, board

    if turn == piece_min:
        best_value = float('inf')
        best_move = None
        for move in generate_moves(piece_min, board):
            value, _ = minimax(piece_max, piece_min, piece_max, move, alpha, beta)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_move
    else:
        best_value = float('-inf')
        best_move = None
        for move in generate_moves(piece_max, board):
            value, _ = minimax(piece_min, piece_min, piece_max, move, alpha, beta)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value, best_move

def best_move(turn, piece_min, piece_max, board):
    logging.info("Finding best move...")
    _, move = minimax(turn, piece_min, piece_max, board)
    return move

# Unit tests
def test_minimax():
    test_board = [['o', '_', 'x'], ['x', 'x', 'o'], ['o', '_', '_']]
    expected_move = [['o', 'o', 'x'], ['x', 'x', 'o'], ['o', '_', '_']]
    actual_move = best_move('o', 'o', 'x', test_board)
    print("Expected Move:", expected_move)
    print("Actual Move:", actual_move)
    assert actual_move == expected_move, "Test case failed!"
    logging.info("Test case passed!")

test_minimax()
