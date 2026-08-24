import tensorflow as tf
import cv2
import numpy as np

def is_square_empty(square, treshold = 20, margin = 0.15):#need a margin cause some of the numbered squares are taken into account as not empty
    h, w = square.shape[:2]
    dy, dx = int(h * margin), int(w * margin)
    center = square[dy:h - dy, dx:w - dx]
    gray = cv2.cvtColor(center, cv2.COLOR_BGR2GRAY)
    std_dev = np.std(gray) #measures how spread out the pixel brightness values are
    return std_dev < treshold, std_dev

def classify_square(square, model, class_names):
    empty, std_dev = is_square_empty(square)
    if empty:
        return "empty"
    rgb = cv2.cvtColor(square, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (160, 160), interpolation = cv2.INTER_LINEAR)
    batched = np.expand_dims(resized, axis = 0)
    prediction = model.predict(batched)
    #print(dict(zip(class_names, prediction[0])))
    predict_index = np.argmax(prediction[0])
    return class_names[predict_index]

if __name__ == "__main__":
    from board_detection import find_board, slice_board
    board = find_board("test_board_cropped6.png")
    squares = slice_board(board)
    #for r, c, square in squares[:64]:
        #empty  = np.std(cv2.cvtColor(square, cv2.COLOR_BGR2GRAY))
        #empty, std_dev = is_square_empty(square)
        #print(f"({r}, {c}): std = {std_dev:.1f}, empty = {empty}")  
    model = tf.keras.models.load_model("models/piece_classifier.keras")
    class_names = ["Black_Bishop", "Black_King", "Black_Knight", "Black_Pawn", "Black_Queen", "Black_Rook",
                   "White_Bishop", "White_King", "White_Knight", "White_Pawn", "White_Queen", "White_Rook"]
    for r, c, square in squares:
        empty, std_dev = is_square_empty(square)
        if empty:
            print(f"({r},{c}): empty")
        else:
            piece = classify_square(square, model, class_names)
            print(f"({r},{c}): {piece}")