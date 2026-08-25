import chess
import chess.engine

def suggest_move(fen, engine_path, think_time = 1.0):
    engine =chess.engine.SimpleEngine.popen_uci(engine_path)
    board = chess.Board(fen)
    limit = chess.engine.Limit(time = think_time)
    result = engine.play(board, limit)
    move = result.move
    move_readable = board.san(move)
    engine.quit()
    return move_readable

if __name__ == "__main__":
    fen = "r1b1rnk1/pp3qp1/2nb1p2/3ppP1Q/3P3N/1P5R/PBPN2PP/R5K1 w - - 0 1"
    engine_path = "engine\stockfish-windows-x86-64-avx2.exe"
    move = suggest_move(fen, engine_path)
    print(f"Suggest move: {move}")