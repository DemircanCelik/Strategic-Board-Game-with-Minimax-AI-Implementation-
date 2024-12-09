import copy

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
        for c in range(self.size):
        # Extract the entire column as a list
            col_line = [self.board[r][c] for r in range(self.size)]
            remove |= self.line_check(col_line, False, c)
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
    def get_new_state(self,start,end):
        #create a new board state with the move
        new_board_state = copy.deepcopy(self.board)
        #get the player making move
        player = self.board[start[0]][start[1]]
        #apply move
        new_board_state[end[0]][end[1]] = player
        new_board_state[start[0]][start[1]] = '*'
        #create a new board with the updated state
        new_board = Board(self.size)
        new_board.board = new_board_state
        new_board.move_count = self.move_count+1
        
        
        return new_board
    
    def get_possible_moves(self,player):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == player:
                    start = (r,c)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions Up, down, left, right
                        new_r, new_c = r + dr, c + dc
                        if 0 <= new_r < self.size and 0 <= new_c < self.size and self.board[new_r][new_c] == '*':
                            end = (new_r, new_c)
                            moves.append((start, end))
                                
        return moves  
    