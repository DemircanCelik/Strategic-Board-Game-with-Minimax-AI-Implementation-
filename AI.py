from CSE_BoardGame import Board


class MiniMaxAgent:
    def __init__(self,max_depth, player):

        self.max_depth = max_depth
        self.player = player
    
    def generate_moves(self,board, player):
        
        moves = []
        pieces = board.find_positions(player)
        
        for r,c in pieces:
                for delta_row, delta_column in [(-1,0), (1,0), (0,-1), (0,1)]:
                    new_row = r + delta_row
                    new_column = c + delta_column
                    if 0 <= new_row < board.size and 0 <= new_column < board.size and board.board[new_row][new_column] == '*':
                        moves.append(((r,c), (new_row, new_column)))
        return moves
        
    def potential_captures(self,board, player, opponent):
        captures = 0
        pieces = board.find_positions(player)
        
        for r,c in pieces:
                for delta_row, delta_column in [(-1,0), (1,0), (0,-1), (0,1)]:
                    new_row = r + delta_row
                    new_column = c + delta_column
                    if 0 <=new_row < board.size and 0 <=new_column < board.size and board.board[new_row][new_column] == opponent:
                        future_row =new_row + delta_row
                        future_column = new_column + delta_column
                        if 0 <= future_row < board.size and 0 <= future_column < board.size and board.board[future_row][future_column] == '*':
                            captures += 1
        return captures
        
        
    
    def evaluate(self, board, AI_player = 'X', opponent = 'O'):
        score = 0
        AI_pieces = len(board.find_positions(AI_player))
        opponent_pieces = len(board.find_positions(opponent))
        score += 10*(AI_pieces - opponent_pieces)
        #positional advantage
        for r in range(board.size):
            for c in range(board.size):
                piece = board.board[r][c]
                if piece == AI_player:
                    score += 5*(board.size -1 -c)
                elif piece == opponent:
                    score -= 5*c
        #mobility
        AI_moves = len(self.generate_moves(board, AI_player))
        opponent_moves = len(self.generate_moves(board, opponent))
        score += 2*(AI_moves - opponent_moves)  
        
        AI_captures = self.potential_captures(board, AI_player, opponent)
        opponent_captures = self.potential_captures(board, opponent, AI_player)
        score += 8*(AI_captures - opponent_captures)
        
        return score

