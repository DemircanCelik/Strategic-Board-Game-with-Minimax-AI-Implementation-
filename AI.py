import copy
import random



#classical recursive minimax algorithm with a-b pruning
def minimax(board, depth, is_maxPlayer, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or board.end_game_check() != 'playing':
        return board.evaluate(), None
    
    current_player = 'X' if is_maxPlayer else 'O'
    possibleMoves = board.get_possible_moves(current_player)
    
    if not possibleMoves:
        return board.evaluate(), None
    
    best_move = possibleMoves[0] if possibleMoves else None
    #minimax of max player
    if is_maxPlayer:
        maxScore = float('-inf')
        for move in possibleMoves:
            boardCopy = copy.deepcopy(board)
            boardCopy.current = current_player
            boardCopy.moves_this_turn = 0
            boardCopy.last_moved_piece_position = None
            start, end = move
            
            try:
                boardCopy.move_piece(start, end)
                score, _ = minimax(boardCopy, depth - 1, False, alpha, beta)
                if score > maxScore:
                    maxScore = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break#pruning
            except ValueError:
                continue
        return maxScore, best_move
    
    #minimax of min player
    else:
        minScore = float('inf')
        for move in possibleMoves:
            boardCopy = copy.deepcopy(board)
            boardCopy.current = current_player
            boardCopy.moves_this_turn = 0
            boardCopy.last_moved_piece_position = None
            start, end = move
            try:
                boardCopy.move_piece(start, end)
                score, _ = minimax(boardCopy, depth - 1, True, alpha, beta)
                if score < minScore:
                    minScore = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
            except ValueError:
                continue
        return minScore, best_move

def aiMove(board):
    #try to make the ai move with different depths to balance between speed and accuracy
    
    depths = [3,4,5]
    
    
    best_Score = float('-inf')
    best_move = None
    
    for depth in depths:
        score, move = minimax(board, depth, True)
        if score > best_Score:
            best_Score = score
            best_move = move
            
    return best_move