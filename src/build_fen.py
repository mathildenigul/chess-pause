from board_detection import find_board, slice_board
from classify_squares import classify_square
import tensorflow as tf
import cv2

#Mapping the 12 class names to FEN letters
#Uppercase is white, lowercase is black

CLASS_TO_FEN = {
    "White_Pawn": "P", "White_Knight": "N", "White_Bishop": "B", "White_Rook": "R", "White_Queen": "Q", "White_King": "K",
    "Black_Pawn": "p", "Black_Knight": "n", "Black_Bishop": "b", "Black_Rook": "r", "Black_Queen": "q", "Black_King": "k"
    }

#Turning the 64(r, c, square) tuples into 8x8 grid of FEN letters or None(empty square)
def classify_board(squares, model, class_names):
    grid = []
    rows, cols = 8, 8
    for _ in range(rows):
        row = []
        for _ in range (cols):
            row.append(None)
        grid.append(row)
    for r, c, square in squares:
        piece = classify_square(square, model, class_names)
        if piece == "empty":
            continue #already None there
        grid[r][c] = CLASS_TO_FEN.get(piece, 0)
    return grid

def grid_to_fen(grid):
    #Turning the x8 grd into the piece placement part of a FEN string
    rows_as_strings = []
    
    for row in grid:
        row_string = ""
        empty_count = 0
        for cell in row:
            if cell is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    row_string += str(empty_count)
                    empty_count = 0
                row_string += cell
        if empty_count > 0:
            row_string += str(empty_count)
        rows_as_strings.append(row_string)
    return ("/").join(rows_as_strings)

def build_fen(image_path, model_path, class_names, side_to_move = "w", board_orientation = "White at bottom"):
    board = find_board(image_path)
    if board_orientation == "Black at bottom":
        board = cv2.rotate(board, cv2.ROTATE_180)
    squares = slice_board(board)
    model = tf.keras.models.load_model(model_path)
    grid = classify_board(squares, model, class_names)
    placement = grid_to_fen(grid)
    
    return f"{placement} {side_to_move} - - 0 1"

if __name__ == "__main__":
    class_names = ["Black_Bishop", "Black_King", "Black_Knight", "Black_Pawn", "Black_Queen", "Black_Rook",
                   "White_Bishop", "White_King", "White_Knight", "White_Pawn", "White_Queen", "White_Rook"]
    fen = build_fen("test_board_cropped6.png", "models/piece_classifier.keras", class_names)
    print(fen)