# Chess Pause

Take a screenshot of a chess position mid-game (e.g. from a masters' game you're
watching) and get an AI-suggested next move — or switch to practice mode and keep
playing the position yourself, without suggestions.

## Status: just started

This project is a work in progress, built solo to practice an end-to-end ML
pipeline: computer vision, a trained classifier, and integrating an external
engine.

## Planned pipeline

1. **Input**: a cropped screenshot of a chess board
2. **Piece classification**: a CNN (transfer learning) classifies each of the 64
   squares as empty or a specific piece
3. **Board reconstruction**: the 64 classifications become a FEN string (the
   standard text format for a chess position)
4. **Move suggestion**: [python-chess](https://python-chess.readthedocs.io/) talks
   to the [Stockfish](https://stockfishchess.org/) engine to suggest the best move
5. **Practice mode**: continue playing from that position yourself, with
   python-chess validating legal moves, no suggestions shown

## Why these scoping choices

- Assumes a clean, roughly top-down screenshot (not a photo at an angle) — this
  keeps board detection tractable in a short timeframe
- Uses an existing chess engine (Stockfish) rather than building one — the
  interesting part of this project is the vision pipeline, not reimplementing a
  solved problem
- Piece classifier is trained on an existing public dataset via transfer
  learning, not from scratch

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Progress log

- [x] Project scaffolding and repo setup
- [ ] Piece classifier trained
- [ ] Board detection + square extraction
- [ ] FEN reconstruction + engine integration
- [ ] Minimal interface with practice mode
