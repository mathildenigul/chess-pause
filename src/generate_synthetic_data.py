"""
Generating a synthetic training dataset by compositing chess piece icons
onto realistic board square backgrounds.

Uses 6 visually distinct open-source piece styles,
so the classifier learns the general concept of a chess piece across
different line weights/shapes, and not just memorizing one exact icon
set. I used a single style at first, tested it and found it generalized poorly
to screenshots using a different site/theme's pieces.

Piece sets used (all from lichess-org/lila, github.com/lichess-org/lila):
  - cburnett  - Colin M.L. Burnett - GPLv2+
  - alpha     - Eric Bentzen - free for personal, non-commercial use
  - fantasy   - MIT
  - horsey    - cham, michael1241 - CC BY-NC-SA 4.0
  - staunty   - sadsnake1 - CC BY-NC-SA 4.0
  - tatiana   - sadsnake1 - CC BY-NC-SA 4.0
I chose staunty and tatiana specifically because chess.com's own
"Neo" piece set is proprietary (not available under an open license),
and community consensus identifies these two as the closest visual
match among openly-licensed alternatives.
All used here for a personal, non-commercial, educational project.

Usage:
    python src/generate_synthetic_data.py
"""

import random
from pathlib import Path
from PIL import Image

PIECE_DIR = Path("piece_svgs")  #contains one subfolder per style
STYLES = ["cburnett", "alpha", "fantasy", "horsey", "staunty", "tatiana"]
OUT_DIR = Path("data_synthetic")
IMAGES_PER_STYLE_PER_CLASS = 60
SQUARE_SIZE = 160

THEMES = [
    ((238, 238, 210), (118, 150, 86)),   #chess.com green
    ((240, 217, 181), (181, 136, 99)),   #lichess brown
    ((234, 233, 210), (75, 115, 153)),   #blue theme
    ((220, 220, 220), (140, 140, 140)),  #gray theme
]

PIECE_TO_CLASS = {
    "wP": "White_Pawn", "wN": "White_Knight", "wB": "White_Bishop",
    "wR": "White_Rook", "wQ": "White_Queen", "wK": "White_King",
    "bP": "Black_Pawn", "bN": "Black_Knight", "bB": "Black_Bishop",
    "bR": "Black_Rook", "bQ": "Black_Queen", "bK": "Black_King",
}


def make_square_background(size, color):
    return Image.new("RGB", (size, size), color)


def composite_piece(background, piece_img, jitter=8, scale_range=(0.75, 0.95)):
    scale = random.uniform(*scale_range)
    piece_size = int(background.width * scale)
    piece_resized = piece_img.resize((piece_size, piece_size))

    offset_x = background.width // 2 - piece_size // 2 + random.randint(-jitter, jitter)
    offset_y = background.height // 2 - piece_size // 2 + random.randint(-jitter, jitter)
    offset_x = max(0, min(offset_x, background.width - piece_size))
    offset_y = max(0, min(offset_y, background.height - piece_size))

    result = background.copy()
    result.paste(piece_resized, (offset_x, offset_y), piece_resized)
    return result


def generate():
    OUT_DIR.mkdir(exist_ok=True)

    for style in STYLES:
        style_dir = PIECE_DIR / style
        for filename in style_dir.glob("*.png"):
            color_code, piece_code = filename.stem[0], filename.stem[1]
            class_name = PIECE_TO_CLASS[f"{color_code}{piece_code}"]
            piece_img = Image.open(filename).convert("RGBA")

            class_dir = OUT_DIR / class_name
            class_dir.mkdir(exist_ok=True)

            for i in range(IMAGES_PER_STYLE_PER_CLASS):
                light, dark = random.choice(THEMES)
                square_color = random.choice([light, dark])
                bg = make_square_background(SQUARE_SIZE, square_color)
                composed = composite_piece(bg, piece_img)
                composed.save(class_dir / f"{style}_{color_code}{piece_code}_{i:03d}.png")

            print(f"{class_name} ({style}, {color_code}): "
                  f"{IMAGES_PER_STYLE_PER_CLASS} images generated")


if __name__ == "__main__":
    generate()