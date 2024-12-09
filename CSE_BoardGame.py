import tkinter as tk
from tkinter import messagebox

from Board import Board

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Strategic Board Game')
        self.board = Board()
        self.move_count = 0   
        self.current = 'X'
        self.selected = None
        self.moves_needed()
        
        #buttons for clicking the cells, pieces etc..
        self.buttons = []
        for r in range(self.board.size):
            row_buttons = []
            for c in range(self.board.size):
                button = tk.Button(self.root, width=4, height=2, command=lambda rr=r, cc=c: self.handle_click(rr, cc))
                button.grid(row=r+1, column=c)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        self.update_display()

    #set the number of moves for the player, one or two based on the pieces on the board
    def moves_needed(self):
        pieces = self.board.find_positions(self.current)
        if len(pieces) == 1:
            self.needed = 1
        else:
            self.needed = 2

    # update the visual information of the board
    def update_display(self):
        for r in range(self.board.size):
            for c in range(self.board.size):
                inf = self.board.board[r][c]
                self.buttons[r][c].config(text=' ' if inf == '*' else inf)

    def swtich_player(self):
        if self.current == 'X':
            self.current = 'O'
        else:
            self.current = 'X'
        self.move_count = 0  # Fixed the typo here
        self.selected = None
        self.moves_needed()
        self.update_display()

    def handle_click(self, r, c):
        if self.board.end_game_check() != 'playing':
            return
        cell = self.board.board[r][c]
        if self.selected is None:
            if cell == self.current:
                self.selected = (r, c)
        else:
            start = self.selected
            end = (r, c)
            if self.board.is_valid_move(self.current, start, end):
                self.board.move_piece(self.current, start, end)
                self.selected = None
                self.move_count += 1
                self.board.capture()
                if self.move_count == self.needed:
                    self.board.move_count += 1
                    status = self.board.end_game_check()
                    if status != 'playing':
                        self.end_game(status)
                        return
                    self.swtich_player()
            else:
                if cell == self.current:
                    self.selected = (r, c)
                else:
                    self.selected = None
        self.update_display()

    def end_game(self, status):
        msg = "Game Over: "
        if status == 'draw':
            msg += "It's a draw."
        elif status == 'p1_win':
            msg += "Player X wins!"
        else:
            msg += "Player 2 wins!"
        
        messagebox.showinfo("Result", msg)

def main():
    root = tk.Tk()
    GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()