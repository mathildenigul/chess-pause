
import cv2
import numpy as np

def is_square_empty(square, treshold = 20, margin = 0.15):#need a margin cause some of the numbered squares are taken into account as not empty
    h, w = square.shape[:2]
    dy, dx = int(h * margin), int(w * margin)
    center = square[dy:h - dy, dx:w - dx]
    gray = cv2.cvtColor(center, cv2.COLOR_BGR2GRAY)
    std_dev = np.std(gray) #measures how spread out the pixel brightness values are
    return std_dev < treshold

if __name__ == "__main__":
    from board_detection import find_board, slice_board
    board = find_board("test_board4.png")
    squares = slice_board(board)
    for r, c, square in squares[:64]:
        std_dev = np.std(cv2.cvtColor(square, cv2.COLOR_BGR2GRAY))
        empty = is_square_empty(square)
        print(f"({r}, {c}): std = {std_dev:.1f}, empty = {empty}")