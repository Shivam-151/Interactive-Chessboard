# Interactive Chessboard Graphics System

**Computer Graphics PBL — Topic 17**

A Python desktop application combining interactive chess gameplay with independently implemented Computer Graphics algorithms. The chess rules are provided by `python-chess`; the graphics algorithms in `src/cg_algorithms.py` are implemented manually for academic demonstration.

## Features

- Interactive 8×8 chessboard with legal-move highlighting, turn status, move history, undo, restart and board flip.
- Player vs Player and Player vs Computer (random legal move) modes.
- Homogeneous 2D transformations: translation, scaling, rotation, reflection and composite matrices.
- Scan-line polygon filling with scanline intersections and filled pixel output.
- DDA and Bresenham line rasterization.
- Midpoint circle drawing.
- Cohen–Sutherland line clipping.
- Chessboard-to-screen and screen-to-board coordinate conversion.
- Separate algorithm visualization panel.

## Requirements

- Python 3.10 or newer recommended
- Tkinter (included with most standard Windows Python installations)
- Matplotlib, NumPy, python-chess

## Windows / VS Code setup

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, use the environment's interpreter directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

## Run algorithm tests

```powershell
python -m unittest discover -s tests -v
```

## Architecture

- `main.py`: Tkinter desktop UI, chessboard rendering and interaction.
- `src/cg_algorithms.py`: manual rasterization, polygon filling, transformations, clipping and coordinate mapping.
- `src/piece_models.py`: geometric silhouette definitions for chess-piece modelling demonstrations.
- `tests/`: unit tests for the independent graphics algorithms.

## Academic mapping

| Faculty concept | Implementation |
|---|---|
| Polygon Filling | `scanline_polygon_fill` — edge intersections, sorted spans, even-odd filling |
| Transformations | `transform_points` — 3×3 homogeneous matrices |
| Object Modelling | Piece silhouettes and geometric primitives |
| Coordinate Systems | `board_to_screen`, `screen_to_board` |
| Additional algorithms | DDA, Bresenham, Midpoint Circle, Cohen–Sutherland |

## Chess rules note

The app uses the `python-chess` package for complete chess legality (including castling, en passant, promotion, check and checkmate). This is deliberately separated from the manually written Computer Graphics algorithms. Pawn promotion defaults to a queen in the click interface. The optional computer opponent currently selects a random legal move; it is a functional demonstration opponent, not a strategic chess engine.

## Team

- Shivam — 1/24/SET/BCS/159
- Deepak — 1/24/SET/BCS/165
- Sameer — 1/24/SET/BCS/154
- Abhay — 1/24/SET/BCS/157

Confirm the Computer Graphics faculty name, course code, and each member's actual task allocation before submission.
