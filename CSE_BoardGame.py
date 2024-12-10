import tkinter as tk
from tkinter import messagebox
from Board import Board
from AI import MiniMaxAgent


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Strategic Board Game')
        
        self.board = Board()
        self.move_count = 0 
        self.ai_agent = MiniMaxAgent(max_depth=3, player='X')
        self.current = self.ai_agent.player  # Now self.current is 'X'
        self.selected = None
        self.previous_piece = None  # Track the previous piece moved
        self.moved_pieces = []  # Track pieces moved in the current turn
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
        self.ai_move()  # AI makes the first move

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

    def switch_player(self):
        if self.current == 'X':
            self.current = 'O'
        else:
            self.current = 'X'
        self.move_count = 0
        self.selected = None
        self.previous_piece = None
        self.moved_pieces = []  # Reset moved pieces
        self.moves_needed()

        # If it's now the AI's turn, make the AI move
        if self.current == self.ai_agent.player:
            self.ai_move()
        else:
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
                if self.previous_piece is None or self.previous_piece != start:
                    if start not in self.moved_pieces:

                        self.board.move_piece(self.current, start, end)
                        self.previous_piece = start
                        self.selected = None
                        self.move_count += 1
                        self.board.capture()
                        self.moved_pieces.append(start)  # Track moved piece
                        if self.move_count == self.needed:
                            self.board.move_count += 1
                            status = self.board.end_game_check()
                            if status != 'playing':
                                self.end_game(status)
                                return
                            self.switch_player()  # Switch to AI's turn if applicable
                    else:
                        messagebox.showwarning("Invalid Move", "You must move a different piece.")
                else:
                    messagebox.showwarning("Invalid Move", "You must move a different piece.")
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
    
    def ai_move(self):
        moves_needed = self.needed
        moved_pieces = []  # Track pieces moved by AI
        while moves_needed > 0:
            move = self.ai_agent.best_move(self.board)
            if move:
                start, end = move
                if start not in moved_pieces:
                    self.board.move_piece(self.ai_agent.player, start, end)
                    self.board.capture()
                    self.board.move_count += 1
                    status = self.board.end_game_check()
                    if status != 'playing':
                        self.end_game(status)
                        return
                    moved_pieces.append(start)  # Track moved piece
                    moves_needed -= 1
                else:
                    break
            else:
                break
        self.switch_player()
        self.update_display()

def main():
    root = tk.Tk()
    GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
