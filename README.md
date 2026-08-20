# Chess Pause

Take a screenshot of a chess position mid-game (e.g. from a masters' game you're watching) and either practice what move you would do next without suggestions or get an AI-suggested next move.

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

Board detection assumes eithe a screenshot with surrounding UI (board is found through edge/contour detection) or an already cropped voard image (it is detected through a board-vs-image are size heuristis and used as a fallback). One limitation now is that the detection for larger images with a small board is more difficult. To avoid such cases a warning was added for large images to crop the images closer to just the board fits.

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

## Progress log

- [x] Project scaffolding and repo setup
- [x] Data prepared with 80/20 train/ validation split
- [x] Piece classifier trained, obtained 75% validation accuracy, with 6 classes, MobileNetV2 transfer learning
- [ ] Board detection + square extraction
- [ ] FEN reconstruction + engine integration
- [ ] Minimal interface with practice mode

## Future work
- Supporting physical board photos, that will require perspective correction and a dataset of 3D piece images captured at different angles
- Empty square detection as a 7th class, because currently the classifier only knows the 6 piece types
- Fine-tuning the frozen MobileNetV2 base on chess-specific data for potentially higher accuracy

