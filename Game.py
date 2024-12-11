import tkinter as tk
from tkinter import messagebox
from Board import Board
from AI import aiMove

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Strategic Board Game')

        self.board = Board()
        self.selected = None
        self.moves_made = []
        

        self.buttons = []
        for r in range(self.board.size):
            row_buttons = []
            for c in range(self.board.size):
                button = tk.Button(self.root, width=4, height=2, command=lambda rr=r, cc=c: self.handle_click(rr, cc))
                button.grid(row=r + 1, column=c)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.update_display()
        self.root.after(1000, self.ai_move)  #ai makes the first move after a delay for better gui interaction

    def update_display(self):
        for r in range(self.board.size):
            for c in range(self.board.size):
                piece = self.board.board[r][c]
                self.buttons[r][c].config(text=' ' if piece == '*' else piece)

    def handle_click(self, r, c):
        if self.board.end_game_check() != 'playing':
            return

        cell = self.board.board[r][c]
        current_pos = (r, c)
        
        if self.selected is None:
            if cell == self.board.current:
                #check if this position was the end position of last move to prevent moving the same piece twice
                if self.moves_made and self.moves_made[-1][1] == current_pos:
                    messagebox.showwarning("Invalid Move", "Cannot move piece that was just moved to this position")
                    return
                self.selected = current_pos
        else:
            start = self.selected
            end = current_pos
            prev_player = self.board.current
            try:
                self.board.move_piece(start, end)
                self.moves_made.append((start, end))
                self.selected = None
                self.update_display()

                if self.board.end_game_check() != 'playing':
                    self.end_game()
                else:
                    if self.board.current == prev_player:
                        self.selected = None
                    else:
                        #clear moves_made when turn changes
                        self.moves_made = []
                        if self.board.current == 'X':
                            self.root.after(500, self.ai_move)
            except ValueError as e:
                messagebox.showwarning("Invalid Move", str(e))
                self.selected = None

    def ai_move(self):
        moves_needed = 2 if len(self.board.getPieces('X')) > 1 else 1
        if moves_needed > 0:
            move = aiMove(self.board)
            if move:
                start, end = move
                self.board.move_piece(start, end)
                self.update_display()
                moves_needed -= 1
                
                #if AI needs to make another move, do it after a delay
                if moves_needed > 0 and self.board.current == 'X':
                    self.root.after(1000, self.ai_move)  # 1 second delay between moves
                elif self.board.end_game_check() != 'playing':
                    self.end_game()
            else:
                if self.board.end_game_check() != 'playing':
                    self.end_game()

    def end_game(self):
        status = self.board.end_game_check()
        if status == 'p1_win':
            messagebox.showinfo("Game Over", "AI Wins!")
        elif status == 'p2_win':
            messagebox.showinfo("Game Over", "Player Wins!")
        elif status == 'draw':
            messagebox.showinfo("Game Over", "It's a draw!")
        self.root.quit()

def main():
    root = tk.Tk()
    GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()