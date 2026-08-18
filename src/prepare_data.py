import random
from pathlib import Path
import shutil

p = Path("archive/Chessman-image-dataset/Chess")
d = Path("data")
SPLIT_RATIO = 0.8 #80%train, 20%val

def prepare():
    for piece_f in p.iterdir():
        if not piece_f.is_dir():
            continue #basically skip stary files only take piece folders
        name_piece = piece_f.name
        images = list(piece_f.iterdir())
        random.shuffle(images)
        split_index = int(len(images) * SPLIT_RATIO)
        train_images = images[:split_index]
        val_images =images[split_index:]
        train_dest = d / "train" / name_piece
        val_dest = d / "val" / name_piece
        train_dest.mkdir(parents = True, exist_ok = True)
        val_dest.mkdir(parents = True, exist_ok = True)
        for i in train_images:
            shutil.copy(i, train_dest)
        for n in val_images:
            shutil.copy(n, val_dest)
        print(f"{piece_f.name}: {len(train_images)} train, {len(val_images)} val")

if __name__ == "__main__":
    prepare()
        