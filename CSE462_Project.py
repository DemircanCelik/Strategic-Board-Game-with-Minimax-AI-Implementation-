import tkinter as tk
from tkinter import messagebox

class Board:
    def __init__(self, size=7):
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.move_count = 0
        self.setup()

    def setup(self):
        # Player A on left column
        self.grid[0][0] = 'X'
        self.grid[2][0] = 'X'
        self.grid[4][6] = 'X'
        self.grid[6][6] = 'X'
        # Player O on right column
        self.grid[0][6] = 'O'
        self.grid[2][6] = 'O'
        self.grid[4][0] = 'O'
        self.grid[6][0] = 'O'

    def positions_of(self, p):
        return [(r,c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == p]

    def valid_move(self, p, start, end):
        (r1,c1) = start
        (r2,c2) = end
        if self.grid[r1][c1] != p: return False
        if not(0 <= r2 < self.size and 0 <= c2 < self.size): return False
        if self.grid[r2][c2] != '.': return False
        if (r1 == r2 and abs(c1-c2)==1) or (c1 == c2 and abs(r1-r2)==1):
            return True
        return False

    def move_piece(self, p, start, end):
        (r1,c1) = start
        (r2,c2) = end
        self.grid[r2][c2] = p
        self.grid[r1][c1] = '.'

    def capture(self):
        to_remove = set()
        # Rows
        for r in range(self.size):
            to_remove |= self.check_line(self.grid[r], True, r)
        # Columns
        for c in range(self.size):
            col = [self.grid[r][c] for r in range(self.size)]
            cap = self.check_line(col, False, c)
            to_remove |= cap
        for (rr,cc) in to_remove:
            self.grid[rr][cc] = '.'

    def check_line(self, line, is_row, idx):
        caps = set()
        i = 0
        while i < self.size:
            if line[i] == '.':
                i += 1
                continue
            p = line[i]
            start = i
            i += 1
            while i<self.size and line[i] == p:
                i+=1
            end = i-1
            left_block = 'WALL' if start==0 else (None if line[start-1]=='.' or line[start-1]==p else line[start-1])
            right_block = 'WALL' if end==self.size-1 else (None if line[end+1]=='.' or line[end+1]==p else line[end+1])

            if left_block and right_block:
                for pos in range(start, end+1):
                    if is_row:
                        caps.add((idx,pos))
                    else:
                        caps.add((pos,idx))
        return caps

    def status(self):
        pA = len(self.positions_of('X'))
        pO = len(self.positions_of('O'))
        if pA==0 and pO==0:
            return 'draw'
        if pA==0 and pO>0:
            return 'p1_lose'
        if pO==0 and pA>0:
            return 'p1_win'
        if pA==1 and pO==1:
            return 'draw'
        if self.move_count>=50:
            if pA==pO:
                return 'draw'
            elif pA>pO:
                return 'p1_win'
            else:
                return 'p2_win'
        return 'ongoing'

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Board Game")
        self.board = Board()
        self.current = 'X'
        self.selected = None
        self.moves_made = 0
        self.set_moves_needed()

        self.info = tk.Label(self.root, text=self.info_text(), font=('Arial', 14))
        self.info.grid(row=0, column=0, columnspan=self.board.size)

        self.btns = []
        for r in range(self.board.size):
            row_btns = []
            for c in range(self.board.size):
                b = tk.Button(self.root, width=4, height=2, command=lambda rr=r, cc=c: self.on_click(rr, cc))
                b.grid(row=r+1, column=c)
                row_btns.append(b)
            self.btns.append(row_btns)
        self.update_display()

    def set_moves_needed(self):
        pcs = self.board.positions_of(self.current)
        self.moves_needed = 1 if len(pcs)==1 else 2

    def info_text(self):
        return f"Player {self.current}, moves left: {self.moves_needed - self.moves_made}"

    def update_display(self):
        for r in range(self.board.size):
            for c in range(self.board.size):
                v = self.board.grid[r][c]
                self.btns[r][c].config(text=' ' if v=='.' else v)
        self.info.config(text=self.info_text())

    def on_click(self, r, c):
        if self.board.status() != 'ongoing':
            return
        cell = self.board.grid[r][c]
        if self.selected is None:
            if cell == self.current:
                self.selected = (r,c)
        else:
            start = self.selected
            end = (r,c)
            if self.board.valid_move(self.current, start, end):
                self.board.move_piece(self.current, start, end)
                self.selected = None
                self.moves_made += 1
                if self.moves_made == self.moves_needed:
                    self.board.capture()
                    self.board.move_count += 1
                    st = self.board.status()
                    if st != 'ongoing':
                        self.end_game(st)
                        return
                    self.switch_player()
            else:
                # If clicked on own piece again, re-select it
                if cell == self.current:
                    self.selected = (r,c)
                else:
                    self.selected = None
        self.update_display()

    def switch_player(self):
        self.current = 'O' if self.current=='X' else 'X'
        self.moves_made = 0
        self.selected = None
        self.set_moves_needed()
        self.update_display()

    def end_game(self, st):
        msg = "Game Over: "
        if st=='draw':
            msg+="It's a draw."
        elif st=='p1_win':
            msg+="Player A wins!"
        elif st=='p2_win':
            msg+="Player O wins!"
        elif st=='p1_lose':
            msg+="Player A loses!"
        elif st=='p2_lose':
            msg+="Player O loses!"
        self.update_display()
        messagebox.showinfo("Result", msg)

def main():
    root = tk.Tk()
    GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
