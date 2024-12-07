import tkinter as tk
from tkinter import messagebox

class Board:
    def __init__(self, size=7):
        self.size = size
        self.board = [['-' for _ in range(size)]for _ in range(size)]
        self.move_cound= 0
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
        for r in range(self.size):
            for c in range (self.size):
                if self.board[r][c] == player:
                    return (r,c)
                
    def move_piece(self, player, start, end):
        #change the positions of pieces on the board and update the previous position with '-'
        (r1,c1) = start
        (r2,c2) = end
        self.board[r2][c2] = player
        self.board[r1][c1] = '-'
                
    def is_valid_move(self, player, start, end):
        (r1,c1) = start
        (r2,c2) = end
        if self.board[r1][c1] !=player:
            return False
        #check the if the move position in the board
        if not( 0 <= r2 < self.size and 0 <= c2 < self.size):
            return False
        #check the if the move position is empty
        if self.board[r2][c2] != '-':
            return False
        if (r1 ==r2 and abs(c1-c2)==1) or (c1 == c2 and abs(r1-r2)==1):
            return True
        return False
    
    def line_check(self, line, is_row, id):
        captured = set()
        i = 0
        while i < self.size:
            if line[i] == '-':
                i +=1
                continue
            player = line[i]
            start = i 
            while i < self.size and line[i] == player:
                i+=1
            


    def capture(self):
        remove = set()
        #columns
        for c in range (self.size):
            for r in range (self.size):
                column= self.board[r][c]
                capture = self.line_check(column, False, c)
                remove |= capture
        for (rr,cc) in remove:
            self.board[rr][cc] = '-'

            