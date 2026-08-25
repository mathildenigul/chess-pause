from build_fen import build_fen
from suggest_move import suggest_move

def analyze_screenshot(image_path, model_path, engine_path, class_names, side_to_move = "w"):
    fen = build_fen(image_path, model_path, class_names, side_to_move = "w")
    move = suggest_move(fen, engine_path, think_time = 1.0)
    return fen, move

if __name__ == "__main__":
    class_names = ["Black_Bishop", "Black_King", "Black_Knight", "Black_Pawn", "Black_Queen", "Black_Rook",
                   "White_Bishop", "White_King", "White_Knight", "White_Pawn", "White_Queen", "White_Rook"]
    image_path = "test_board_cropped6.png"
    model_path = "models/piece_classifier.keras"
    engine_path = "engine\stockfish-windows-x86-64-avx2.exe"
    
    fen, move = analyze_screenshot(image_path, model_path, engine_path, class_names, side_to_move = "w")
    print(f"Position: {fen}")
    print(f"Suggested move: {move}")