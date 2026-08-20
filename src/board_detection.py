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
    
    return board

if __name__ == "__main__":
    board = find_board("test_board3.png")
    cv2.imwrite("test_board_cropped3.png", board)
    print(f"Board found, size: {board.shape}")