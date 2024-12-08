import tkinter as tk
from tkinter import messagebox
from AI import MiniMaxAgent


class Board:
    def __init__(self, size=7):
        self.size = size
        self.board = [['*' for _ in range(size)]for _ in range(size)]
        self.move_count= 0
        self.setup()

    def setup(self):
        self.board[0][0] = 'X'
        self.board[2][0] = 'X'
        self.board[4][6] = 'X'
        self.board[6][6] = 'X'

        self.board[0][6] = 'O'
        self.board[2][6] = 'O'
        self.board[4][0] = 'O'
        self.board[6][0] = 'O'
        
    def find_positions(self, player):
        positions = []
        for r in range(self.size):
            for c in range (self.size):
                if self.board[r][c] == player:
                    positions.append((r,c))
        return positions
                
    def move_piece(self, player, start, end):
        #change the positions of pieces on the board and update the previous position with '-'
        (r1,c1) = start
        (r2,c2) = end
        self.board[r2][c2] = player
        self.board[r1][c1] = '*'
                
    def is_valid_move(self, player, start, end):
        (r1,c1) = start
        (r2,c2) = end
        if self.board[r1][c1] !=player:
            return False
        #check the if the move position in the board
        if not( 0 <= r2 < self.size and 0 <= c2 < self.size):
            return False
        #check the if the move position is empty
        if self.board[r2][c2] != '*':
            return False
        if (r1 ==r2 and abs(c1-c2)==1) or (c1 == c2 and abs(r1-r2)==1):
            return True
        return False
    
    #check lines for captures
    def line_check(self, line, is_row, id):
        captured = set()
        i = 0
        while i < self.size:
            if line[i] == '*':
                i +=1
                continue
            player = line[i]
            start = i 
            i+=1
            while i < self.size and line[i] == player:
                i+=1
            end = i-1
            #check if the players piece is blocked by wall or enemy
            
            if(start== 0 ):
                left = 'WALL'
            elif line[start-1] == '*' or line[start-1] == player:
                left = None
            else:
                #enemy piece
                left = line[start-1]
            
            #right check
            if end == self.size-1:
                right = 'WALL'
            elif line[end+1] == '*' or line[end+1] == player:
                right = None
            else:
                right = line[end+1]
            #capture check
            if left and right:
                for positions in range (start, end+1):
                    if is_row:
                        captured.add((id, positions))
                    else:
                        captured.add((positions, id))
        return captured
            
                
            
            


    def capture(self):
        remove = set()
        #columns
        for c in range (self.size):
            for r in range (self.size):
                column= self.board[r][c]
                remove |=self.line_check(column, False, c)
        #rows
        for r in range(self.size):
            row = self.board[r]
            remove |= self.line_check(row, True, r)
        for (rr,cc) in remove:
            self.board[rr][cc] = '*'


    def end_game_check(self):
        piecesX= len(self.find_positions('X'))
        piecesO= len(self.find_positions('O'))
        
        if piecesX==0 and piecesO==0 :
            return 'draw'
        if piecesX==0 and piecesO>0:
            return 'p2_win'
        if piecesO== 0 and piecesX>0:
            return 'p1_win'
        if piecesX==1 and piecesO==1:
            return 'draw'
        if self.move_count>=50:
            if piecesX==piecesO:
                return 'draw'
            elif piecesX>piecesO:
                return 'p1_win'
            else:
                return 'p2_win'
        return 'playing'
    
class GUI:
    def __init__(self,root):
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
            for c in range (self.board.size):
                button = tk.Button(self.root, width = 4, height = 2, command = lambda rr=r, cc=c: self.handle_click(rr,cc))
                button.grid(row=r+1, column=c)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        self.update_display()
        
  
    
                


    #set the number of moves for the player,  one or two based on the pieces on the board
    def moves_needed(self):
        pieces = self.board.find_positions(self.current)
        if len(pieces)==1:
            self.needed = 1
        else:
            self.needed = 2
  
        
    
    #update the visual information of the board
    def update_display(self):
        for r in range (self.board.size):
            for c in range (self.board.size):
                inf = self.board.board[r][c]
                self.buttons[r][c].config(text=' ' if inf=='*' else inf)
    
    def swtich_player(self):
        if self.current == 'X':
            self.current = 'O'
        else:
            self.current = 'X'
        self.moves_count = 0
        self.selected = None
        self.moves_needed()
        self.update_display()
        
                
    def handle_click(self, r, c):
        if self.board.end_game_check() != 'playing':
            return
        cell = self.board.board[r][c]
        if self.selected is None:
            if cell == self.current:
                self.selected = (r,c)
        else:
            start = self.selected
            end = (r,c)
            if self.board.is_valid_move(self.current, start, end):
                self.board.move_piece(self.current, start, end)
                self.selected = None
                self.move_count +=1
                self.board.capture()
                if self.move_count == self.needed:
                    self.board.move_count +=1
                    status = self.board.end_game_check()
                    if status != 'playing':
                        self.end_game(status)
                        return
                    self.swtich_player()
            else:
                if cell== self.current:
                    self.selected= (r,c)
                else:
                    self.selected = None
        self.update_display()
        
    def end_game(self, status):
        msg= "Game Over: "
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
        
    