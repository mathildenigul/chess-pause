import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_board(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ =  cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    square_contours = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        aspect_ratio = w / h
        if h > 0 and 0.9 < aspect_ratio < 1.1:
            square_contours.append(c)
    largest = max(square_contours, key = cv2.contourArea) #contour arrays of poiints, that's why they key
    x, y, w, h = cv2.boundingRect(largest)
    board_area = w * h
    image_area = img.shape[0] * img.shape[1]
    if board_area < image_area * 0.1:
        print("Warning: could not confidently detect a board in this image.")
        print("If this is a full screenshot, try cropping it closer, so just the board fits.")
        print(f"Ratio: {(board_area / image_area):.2f} ")
        return img
    board = img[y:y+h, x:x+w]
    if board.shape[0] // 8 < 80:
        print("Warning: board resolution is low.")
        f"({board.shape[0]}px, {board.shape[0]//8}px per square). "
        f"Classification may be unreliable below 80px per square."
    
    return board

def slice_board(board):
    height, width, _ = board.shape
    square_h = height // 8
    square_w = width // 8
    
    squares = []
    for r in range(8):
        for c in range(8):
            y = r * square_h
            x = c * square_w
            square = board[y:y + square_h, x:x + square_w]
            squares.append((r, c, square))
        
    return squares
    
if __name__ == "__main__":
    board = find_board("test_board1.jpg")
    cv2.imwrite("test_board_cropped1.png", board)
    print(f"Board found, size: {board.shape}")
    squares = slice_board(board)
    print(f"Has {len(squares)} squares")
    for i, (r,c, square) in enumerate(squares[:5]):
        cv2.imwrite(f"debug_square_{i}.png", square)