from Board import Board
import copy




class MiniMaxAgent:
    def __init__(self,max_depth, player):
        self.max_depth = max_depth
        self.player = player
    
    def generate_moves(self,board, player):
        return board.get_possible_moves(player)        
        
    def potential_captures(self,board, player, opponent):
        captures = set()
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] == player:
                    captures |= board.line_check([board.board[r][i] for i in range(board.size)], True, r)
                    captures |= board.line_check([board.board[i][c] for i in range(board.size)], False, c)        
        return captures
        
    
    def evaluate(self, board, AI_player='X', opponent='O'):
        score = 0
        AI_pieces = len(board.find_positions(AI_player))
        opponent_pieces = len(board.find_positions(opponent))
        score += 10 * (AI_pieces - opponent_pieces)

        for r in range(board.size):
            for c in range(board.size):
                piece = board.board[r][c]
                if piece == AI_player:
                    score += 5 * (board.size - 1 - c)
                elif piece == opponent:
                    score -= 5 * c

        AI_moves = len(board.get_possible_moves(AI_player))
        opponent_moves = len(board.get_possible_moves(opponent))
        score += 3 * (AI_moves - opponent_moves)

        AI_captures = self.potential_captures(board, AI_player, opponent)
        opponent_captures = self.potential_captures(board, opponent, AI_player)
        score += 8 * (len(AI_captures) - len(opponent_captures))

        return score


    

    def simulate_move(self, board, move, player):
        start, end = move
        new_board = board.get_new_state(start,end)
        new_board.capture()

        return new_board
        
    
    def minimax(self,board,depth,is_maximizing, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or board.end_game_check() != 'playing':
            return self.evaluate(board), None

        if is_maximizing:
            bestScore = float('-inf')
            best_movement = None
            possible_moves = board.get_possible_moves(self.player)
            for start,end in possible_moves:
                child = board.get_new_state(start,end)
                tmp = self.minimax(child, depth - 1, False, alpha, beta)[0]
                if tmp > bestScore:
                    bestScore = tmp
                    best_movement = start,end

                if alpha >= beta:
                    break
                alpha = max(alpha, bestScore)
            return bestScore, best_movement
        

        else:
            bestScore = float('inf')
            best_movement = None
            opponent = 'O' if self.player == 'X' else 'X'
            possible_moves = board.get_possible_moves(opponent)
            for start,end in possible_moves:
                child = board.get_new_state(start,end)
                tmp = self.minimax(child, depth - 1, True, alpha, beta)[0]
                if tmp < bestScore:
                    bestScore = tmp
                    best_movement = (start,end)

                if alpha >= beta:
                    break
                beta = min(beta, bestScore)

            return bestScore, best_movement
            
        
        
                
            
    def best_move(self, board):
        best_score = float('-inf')
        best_move = None
        possible_moves = board.get_possible_moves(self.player)
        for move in possible_moves:
            new_board = copy.deepcopy(board)
            new_board.move_piece(self.player, move[0], move[1])
            new_board.capture()
            score, _ = self.minimax(new_board, self.max_depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move