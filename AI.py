from Board import Board




class MiniMaxAgent:
    def __init__(self,max_depth, player):
        self.max_depth = max_depth
        self.player = player
    
    def generate_moves(self,board, player):
        
        
        
        
    def potential_captures(self,board, player, opponent):
        
        
        
    
    def evaluate(self, board, AI_player = 'X', opponent = 'O'):
    

    def simulate_move(self, board, move, player):
        
    
    def minimax(self,board,depth,is_maximizing):
        if depth == 0 or board.end_game_check() != 'playing':
            return self.evaluate(board)
        if is_maximizing:
            bestScore = float('-inf')
            possibleMoves = board.get_possible_moves(self.player)
            for move in possibleMoves:
                child = board.get_new_state(move)
                tmp = self.minimax(child,depth-1,False)
            
            
        
        
                
            
    def best_move(self, board):
        bestScore = float('-inf')
        move = None
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] == '*':
                    new_board = board.copy()
                    
                    
        
        