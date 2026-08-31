# Chess Pause

Upload a screenshot of a chess position mid-game (e.g. from a masters' game you're watching or a puzzle) and either practice what move you would make next or get an AI-suggested next move.

**Live pipeline:** screenshot -> board detection (OpenCV) -> piece classification (transfer learning CNN, MobileNetV2, 12 classes) -> FEN reconstruction -> Stockfish move suggestion, wrapped in a Streamlit interface with a playable board.


## Demo
<img width="958" height="1233" alt="Demo1" src="https://github.com/user-attachments/assets/e2b66997-9b9f-495c-bb2e-c75b210d53da" />
<img width="874" height="1259" alt="Demo2" src="https://github.com/user-attachments/assets/f268492c-1a49-4763-9014-ecfb90c29235" />
<img width="779" height="732" alt="Demo3" src="https://github.com/user-attachments/assets/9d7a8924-8ed9-4731-9588-72b006a1977c" />


## Try it

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

## Scope

Digital board screenshots (lichess, chess.com, diagram images). Not using physical board photos because they are a known extension that require additional work or perspective correction and also a different training dataset.

### Why these scoping choices

- Assumes a clean, roughly top-down screenshot (not a photo at an angle) — this keeps board detection tractable in a short timeframe
- Uses an existing chess engine (Stockfish) rather than building one — the interesting part of this project is the vision pipeline, not reimplementing a solved problem
- Piece classifier is trained on an existing public dataset via transfer learning, not from scratch

## Status: just started

This project is a work in progress, built solo to practice an end-to-end ML
pipeline: computer vision, a trained classifier, and integrating an external
engine.

### Known limitation, handled

Board detection assumes eithe a screenshot with surrounding UI (board is found through edge/contour detection) or an already cropped board image (it is detected through a board-vs-image are size heuristis and used as a fallback). One limitation now is that the detection for larger images with a small board is more difficult. To avoid such cases a warning was added for large images to crop the images closer to just the board fits.
Also, tested and reliable on boards where each square is roughly 80px(normal full-window screenshots) or larger, small embedded diagrams (<50px) may misclassify, since upscaling the model's 160x160 iput size causes heavy blur. Fixing it would mean training on deliberately low-resolution synthetic examples.

## Planned pipeline

1. **Input**: a cropped screenshot of a chess board
2. **Piece classification**: a CNN (transfer learning) classifies each of the 64 squares as empty or a specific piece
3. **Board reconstruction**: the 64 classifications become a FEN string (the standard text format for a chess position)
4. **Move suggestion**: [python-chess](https://python-chess.readthedocs.io/) talks to the [Stockfish](https://stockfishchess.org/) engine to suggest the best move
5. **Practice mode**: continue playing from that position yourself, with
   python-chess validating legal moves, no suggestions shown


## Setup

```bash
python -m venv .venv
source .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Dataset

**Original approach** - Kaggle "chessman image dataset", real photographed pieces caused a train/ inference domin  mismatch: the model performed quite poorly on flat digital board icons, which was the actual use case. It was confirmed through low-confidence predictions on real chess.com/ lichess screenshots (e.g. 47% Pawn vs 37% Queen on an actual queen piece).

**Fix**: generated a synthetic dataset insted by compositing open-source piece icons onto multiple realistic board-square color themes with randomized position/scale. **Uses 4 visually distinct piece styles**, since an early versio trained on a single style (lichess's default) generalized poorly to other sites/themes.

Styles used (`piece_svgs/<style>/`, all from [lichess-org/lila](https://github.com/lichess-org/lila/tree/master/public/piece), used here for a personal, non-commercial, educational project):
- `cburnett`- Colin M.L. Burnett - GPLv2+
- `alpha` - Eric Bentzen - free for personal, non-commercial use
- `fantasy` - MIT
- `horsey` - cham, michael1241 - CC BY-NC-SA 4.0
- `staunty` - sadsnake1 - CC BY-NC-SA 4.0
- `tatiana` - sadsnake1 - CC BY-NC-SA 4.0

chess.com-s own "Neo" piece set is proprietary and not available under as open license, so that is why it is not used irectly here. `staunty`  and `tatiana` were added specifically because they are the closest visual match to chess.com's Neo style among the openly-licensed alternatives.

```bash
py src/generate_synthetic_data.py   #produces data_synthetic/<Piece>/*.png
```
Then point `src/prepare_data.py`'s `SOURCE` constant at `data_synthetic` and re-run the split before retraining with `train_classifier.py`. Neither `data_synthetic/` nor `data/` are committe (see `.gitignore`), both are fully reproucible from `piece_svgs/` and the generator script. 

## Progress log

- [x] Project scaffolding and repo setup
- [x] Data prepared with 80/20 train/ validation split
- [x] Piece classifier trained, obtained 75% validation accuracy, with 6 classes, MobileNetV2 transfer learning
- [x] Board detection + square extraction
- [x] FEN reconstruction + engine integration
- [ ] Minimal interface with practice mode

## Future work
- Supporting physical board photos, that will require perspective correction and a dataset of 3D piece images captured at different angles
- Empty square detection as a 7th class, because currently the classifier only knows the 6 piece types
- Fine-tuning the frozen MobileNetV2 base on chess-specific data for potentially higher accuracy
- Train model on deliberately low-resolution synthetic examples also to be able to classify pieces even on low-resolution images.
