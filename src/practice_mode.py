import chess

def practice_mode(fen):
    board = chess.Board(fen)
    while not board.is_game_over():
        print(board)
        print([board.san(m) for m in board.legal_moves])
        print() #a blank line just for readability
        move_input = input("Your move (or 'quit'): ")
        if move_input == "quit":
            break
        try:
            board.push_san(move_input)
        except ValueError:
            print("Illegal move, please try again.")
            continue
    print()
    print(board)
    if board.is_game_over():
        print(board.result())
        
if __name__ == "__main__":
    fen = "r1b1rnk1/pp3qp1/2nb1p2/3ppP1Q/3P3N/1P5R/PBPN2PP/R5K1 w - - 0 1"
    practice_mode(fen)
