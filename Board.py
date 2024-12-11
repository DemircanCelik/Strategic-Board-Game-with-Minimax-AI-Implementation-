class Board:
    def __init__(self, size=7):
        self.size = size
        self.board = [['*' for i in range(size)] for j in range(size)]
        self.move_count = 0



        # Initial setup
        self.board[0][0] = 'X'
        self.board[2][0] = 'X'
        self.board[4][6] = 'X'
        self.board[6][6] = 'X'

        self.board[0][6] = 'O'
        self.board[2][6] = 'O'
        self.board[4][0] = 'O'
        self.board[6][0] = 'O'
        
        self.current = 'X'
        self.move_count = 0
        self.last_move = None
        
        self.last_moved_piece_position = None
        self.moves_this_turn = 0
        

    def getPieces(self, player):
        pieces = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == player:
                    pieces.append((r, c))
        return pieces

    

    def is_valid_move(self,start, end):
        (r1, c1) = start
        (r2, c2) = end
        #check piece belongs to player
        if self.board[r1][c1] != self.current:
            return False
        #check move in the board
        if not (0 <= r2 < self.size and 0 <= c2 < self.size):
            return False
        #check target is empty
        if self.board[r2][c2] != '*':
            return False
        #move must max 1 step
        if (r1 == r2 and abs(c1 - c2) == 1) or (c1 == c2 and abs(r1 - r2) == 1):
            return True
        return False
    
    def move_piece(self, start, end):
        if not self.is_valid_move(start, end):
            raise ValueError('Invalid move')
        player_pieces = self.getPieces(self.current)
        if len(player_pieces) > 1:
            if self.moves_this_turn == 0:
                self.last_moved_piece_position = start
                self.moves_this_turn = 1
            elif self.moves_this_turn == 1:
                if start == self.last_moved_piece_position:
                    raise ValueError('You cannot move the same piece twice.')
                self.moves_this_turn = 2
            else:
                raise ValueError('You cannot make more than 2 moves.')
        else:
            if self.moves_this_turn > 0:
                raise ValueError('You cannot make more than 1 move.')
            self.moves_this_turn = 1

        (r1, c1) = start
        (r2, c2) = end
        self.board[r2][c2] = self.current
        self.board[r1][c1] = '*'
        self.capture()

        if self.moves_this_turn == (2 if len(player_pieces) > 1 else 1):
            # Switch player
            self.current = 'X' if self.current == 'O' else 'O'
            self.moves_this_turn = 0
            self.last_moved_piece_position = None
            self.move_count += 1

        # Store last move
        self.last_move = (start, end)
        
        
    #check if a line has a capture
    def line_check(self, line, is_row, idx):
        captured = set()
        i = 0
        while i < self.size:
            if line[i] == '*':
                i += 1
                continue
            player = line[i]
            start = i
            i += 1
            while i < self.size and line[i] == player:
                i += 1
            end = i - 1

            #left wall
            if start == 0:
                left = 'WALL'
            else:
                left = line[start - 1] if (line[start - 1] != '*' and line[start - 1] != player) else None

            #right wall
            if end == self.size - 1:
                right = 'WALL'
            else:
                right = line[end + 1] if (line[end + 1] != '*' and line[end + 1] != player) else None

            #capture cond.
            if left and right:
                for pos in range(start, end + 1):
                    if is_row:
                        captured.add((idx, pos))
                    else:
                        captured.add((pos, idx))
        return captured

    def capture(self):
        remove = set()
        #columns
        for c in range(self.size):
            col_line = [self.board[r][c] for r in range(self.size)]
            remove |= self.line_check(col_line, False, c)

        #rows
        for r in range(self.size):
            row_line = self.board[r]
            remove |= self.line_check(row_line, True, r)

        for (rr, cc) in remove:
            self.board[rr][cc] = '*'

    def end_game_check(self):
        piecesX = len(self.getPieces('X'))
        piecesO = len(self.getPieces('O'))

        if piecesX == 0 and piecesO == 0:
            return 'draw'
        if piecesX == 0 and piecesO > 0:
            return 'p2_win'
        if piecesO == 0 and piecesX > 0:
            return 'p1_win'
        if piecesX == 1 and piecesO == 1:
            return 'draw'
        if self.move_count >= 50:
            if piecesX == piecesO:
                return 'draw'
            elif piecesX > piecesO:
                return 'p1_win'
            else:
                return 'p2_win'
        return 'playing'

    def copy(self):
        new_board = Board(self.size)
        new_board.board = [row[:] for row in self.board]
        new_board.move_count = self.move_count
        return new_board

    def get_possible_moves(self, player):
        moves = []
        pieces = self.getPieces(player)
        filtered_pieces = []
        
        #filter pieces based on:
        #if it was the last moved piece in this turn
        #if it was the end position of the last move, to prevent moving the same piece twice
        for piece in pieces:
            if (self.moves_this_turn == 1 and piece == self.last_moved_piece_position) or \
               (self.last_move and piece == self.last_move[1]):
                continue
            filtered_pieces.append(piece)
        
        # Generate moves only for filtered pieces
        for r, c in filtered_pieces:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == '*':
                    moves.append(((r, c), (nr, nc)))
        return moves

    def evaluate(self):
        aiPieces = len(self.getPieces('X'))
        opponentPieces = len(self.getPieces('O'))
        if opponentPieces == 0:
            return float('inf')
        if aiPieces == 0:
            return float('-inf')
        
        if self.move_count >= 50:
            if aiPieces == opponentPieces:
                return 0
            elif aiPieces > opponentPieces:
                return float('inf')
            else:
                return 0
            
        return aiPieces - opponentPieces + len(self.get_possible_moves('X'))