import tkinter as tk
from tkinter import messagebox

class StrategicBoardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Strategic Board Game")
        self.board_size = 7
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "Player 1"
        self.pieces = {"Player 1": "X", "Player 2": "O"}
        self.selected_piece = None
        self.moves_made = 0

        self.initialize_board()
        self.create_board()

    def initialize_board(self):
        # Set up initial positions for Player 1 and Player 2
        self.board[0][0] = self.pieces["Player 1"]
        self.board[2][0] = self.pieces["Player 1"]
        self.board[4][6] = self.pieces["Player 1"]
        self.board[6][6] = self.pieces["Player 1"]

        self.board[0][6] = self.pieces["Player 2"]
        self.board[2][6] = self.pieces["Player 2"]
        self.board[4][0] = self.pieces["Player 2"]
        self.board[6][0] = self.pieces["Player 2"]

    def create_board(self):
        self.buttons = []
        for j in range(self.board_size):  # Satırlar
            row = []
            for i in range(self.board_size):  # Sütunlar
                btn = tk.Button(
                    self.root,
                    text=self.board[j][i],
                    width=4,
                    height=2,
                    command=lambda y=j, x=i: self.handle_click(y, x),
                )
                btn.grid(row=j, column=i)
                row.append(btn)
            self.buttons.append(row)

        self.turn_label = tk.Label(self.root, text=f"Turn: {self.current_player}")
        self.turn_label.grid(row=self.board_size, column=0, columnspan=self.board_size)

    def update_board(self):
        for j in range(self.board_size):  # Satırlar
            for i in range(self.board_size):  # Sütunlar
                self.buttons[j][i].config(text=self.board[j][i])
        self.turn_label.config(text=f"Turn: {self.current_player}")

    def handle_click(self, y, x):
        if self.selected_piece:
            sy, sx = self.selected_piece
            if self.is_valid_move(sy, sx, y, x):
                self.board[y][x] = self.board[sy][sx]
                self.board[sy][sx] = ""
                self.check_captures(y, x)
                self.moves_made += 1
                self.selected_piece = None
                if self.check_game_end():
                    return
                self.switch_turn()
            else:
                messagebox.showinfo("Invalid Move", "You can't move there!")
        elif self.board[y][x] == self.pieces[self.current_player]:
            self.selected_piece = (y, x)
        else:
            messagebox.showinfo("Invalid Selection", "Select a valid piece to move!")

        self.update_board()

    def is_valid_move(self, sy, sx, y, x):
        return (sy == y or sx == x) and abs(sy - y + sx - x) == 1
    
    def check_captures(self, y, x):
        opponent = "Player 1" if self.current_player == "Player 2" else "Player 1"
        opponent_piece = self.pieces[opponent]
        player_piece = self.pieces[self.current_player]
        captures = []

        # Horizontal checks
        if x > 0 and x < self.board_size - 1:
            if self.board[y][x - 1] == opponent_piece and (x - 2 < 0 or self.board[y][x - 2] == player_piece):
                captures.append((y, x - 1))
            if self.board[y][x + 1] == opponent_piece and (x + 2 >= self.board_size or self.board[y][x + 2] == player_piece):
                captures.append((y, x + 1))
            if (
                self.board[y][x - 1] == opponent_piece and
                self.board[y][x - 2] == opponent_piece and
                (x - 3 < 0 or self.board[y][x - 3] == player_piece) and
                (x + 1 >= self.board_size or self.board[y][x + 1] == player_piece)
            ):
                captures.append((y, x - 1))
                captures.append((y, x - 2))

        # Vertical checks
        if y > 0 and y < self.board_size - 1:
            if self.board[y - 1][x] == opponent_piece and (y - 2 < 0 or self.board[y - 2][x] == player_piece):
                captures.append((y - 1, x))
            if self.board[y + 1][x] == opponent_piece and (y + 2 >= self.board_size or self.board[y + 2][x] == player_piece):
                captures.append((y + 1, x))
            if (
                self.board[y - 1][x] == opponent_piece and
                self.board[y - 2][x] == opponent_piece and
                (y - 3 < 0 or self.board[y - 3][x] == player_piece) and
                (y + 1 >= self.board_size or self.board[y + 1][x] == player_piece)
            ):
                captures.append((y - 1, x))
                captures.append((y - 2, x))

        # Remove captured pieces
        for cy, cx in captures:
            self.board[cy][cx] = ""


    def switch_turn(self):
        self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"

    def check_game_end(self):
        player1_pieces = sum(row.count(self.pieces["Player 1"]) for row in self.board)
        player2_pieces = sum(row.count(self.pieces["Player 2"]) for row in self.board)

        if player1_pieces == 0 and player2_pieces == 0:
            messagebox.showinfo("Game Over", "It's a Draw! Both players have no pieces.")
            return True
        elif player1_pieces == 0:
            messagebox.showinfo("Game Over", "Player 2 wins!")
            return True
        elif player2_pieces == 0:
            messagebox.showinfo("Game Over", "Player 1 wins!")
            return True
        elif self.moves_made >= 50:
            if player1_pieces > player2_pieces:
                messagebox.showinfo("Game Over", "Player 1 wins by having more pieces!")
            elif player2_pieces > player1_pieces:
                messagebox.showinfo("Game Over", "Player 2 wins by having more pieces!")
            else:
                messagebox.showinfo("Game Over", "It's a Draw!")
            return True
        return False

# Main Application Loop
if __name__ == "__main__":
    root = tk.Tk()
    game = StrategicBoardGame(root)
    root.mainloop()
