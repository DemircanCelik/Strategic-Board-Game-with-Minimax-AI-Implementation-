
# Strategic Board Game with AI

This project is a turn-based strategic board game implemented in Python using the Tkinter library for the graphical user interface (GUI). The game features both human and AI players, by using the Minimax algorithm with Alpha-Beta Pruning to make intelligent decisions. It also includes advanced game logic, such as piece captures and turn-based rules requiring multiple moves for players with more than one piece.

## Key Features
- Interactive GUI: A clean and responsive interface built with Tkinter, allowing players to interact with the game board.
- AI Opponent: An AI player powered by the Minimax algorithm that evaluates board states and chooses optimal moves.

## Game Mechanics
- Players must make two subsequent moves with different pieces if they have more than one piece; otherwise, only one move is allowed.

- Automatic piece capture logic when pieces are surrounded by walls or opponent pieces.

- Rule-Based Turns: Enforces the rule of alternating turns between the player and the AI.


## Dynamic Evaluation
- The AI evaluates board states based on factors such as:
- Piece advantage.
- Positional advantage.
- Mobility and capture potential.
## How to Play

- Run the game using the Game.py file.

- The AI (Player 'X') starts the game.

- The player (Player 'O') makes their moves by clicking on their pieces and selecting valid destinations.

- The game ends when one player has no pieces left, or after 50 turns:

- The player with the most pieces wins.

- A draw occurs if both players have the same number of pieces.
## Tech Stack:

- Python: Core programming language for game logic and AI.

- Tkinter: For GUI implementation.

- Algorithm: Minimax with Alpha-Beta Pruning for AI decision-making.
