from agent import Agent
import numpy as np

class Search(Agent):
    def make_move(self, board):
        board_size = len(board)
        depth = 3

        if np.sum(board == 0) == board_size * board_size: # 棋盘上完全是空的，默认下在中间吧
            return (board_size//2, board_size//2)

        max_score = float('-inf')
        best_move = None

        moves = self.getAllMoves(board)

        for move in moves:
            x, y = move
            board[x][y] = self.player #模拟下棋
            score = self.alpha_beta(board, False, 2, float('-inf'), float('inf'))
            board[x][y] = 0 #还原
            if score > max_score:
                max_score = score
                best_move = move
        return best_move

    def alpha_beta(self, board, to_max, level, alpha, beta):

        if level == 0 or self.check_win(board):
            return self.evaluate(board)
        moves = self.getAllMoves(board)
        if to_max:
            max_val = float('-inf')
            for move in moves:
                x, y = move
                board[x][y] = self.player
                val = self.alpha_beta(board, False, level - 1, alpha, beta)
                board[x][y] = 0
                max_val = max(max_val, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return max_val
        else:
            min_val = float('inf')
            for move in moves:
                x, y = move
                board[x][y] = self.opponent
                val = self.alpha_beta(board, True, level - 1, alpha, beta)
                board[x][y] = 0
                min_val = min(min_val, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return min_val

    def getAllMoves(self, board): # 改成遍历棋子周围的那些点，这样可以少搜索一些点，剪枝效率更高
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
            (0, -1),
            (-1, 0),
            (-1, -1),
            (-1, 1)
        ]
        board_size = len(board)
        moves = []
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] != 0:
                    for dx,dy in directions:
                            new_x, new_y = i + dx, j + dy
                            if 0 <= new_x < board_size and 0 <= new_y < board_size and board[new_x][new_y] == 0:
                                if (new_x, new_y) not in moves:
                                    moves.append((new_x, new_y))
        scored_moves = []
        # 初次判断，直接判断这个节点的重要性
        for i, j in moves:
            temp_score = self.judge_count(board, (i, j), self.player)
            scored_moves.append((temp_score, (i, j)))
        scored_moves.sort(reverse=True, key=lambda x: x[0])
        return [move for _, move in scored_moves]
    
    def judge_count(self, board, loc, player):
        row, col = loc
        # if board[row][col] != player:
        #     return 0
        board_size = len(board)
        score = 0
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]

        for dx, dy in directions:
            count = 1
            ends = 0

            x, y = row + dx, col + dy
            while 0 <= x < board_size and 0 <= y < board_size:
                if board[x][y] == player:
                    count += 1
                else:
                    if board[x][y] != 0:
                        ends += 1
                    break
                x, y = x + dx, y + dy

            x, y = row - dx, col - dy
            while 0 <= x < board_size and 0 <= y < board_size:
                if board[x][y] == player:
                    count += 1
                else:
                    if board[x][y] != 0:
                        ends += 1
                    break
                x, y = x - dx, y - dy

            if count >= 5:
                score += 100000
            elif count == 4:
                if ends == 0:
                    score += 10000
                elif ends == 1:
                    score += 1000
            elif count == 3:
                if ends == 0:
                    score += 1000
                elif ends == 1:
                    score += 100
            elif count == 2:
                if ends == 0:
                    score += 100
                elif ends == 1:
                    score += 10
            elif count == 1:
                if ends == 0:
                    score += 10
                elif ends == 1:
                    score += 1
        return score

    def evaluate(self, board):
        board_size = len(board)
        score = 0
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == self.player:
                    score += self.judge_count(board, (i, j), self.player)
                elif board[i][j] == self.opponent:
                    score -= 1.32 * self.judge_count(board, (i, j), self.opponent)
        return score

    def check_win(self, board):
        board_size = len(board)
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] != 0:
                    player = board[i][j]
                    for dx, dy in directions:  # 用了gomoku.py中的chech_win类似写法，但是要遍历所有地方是否有一个能获胜，有则return
                        count = 1
                        x, y = i + dx, j + dy
                        while 0 <= x < board_size and 0 <= y < board_size and board[x][y] == player:
                            count += 1
                            x, y = x + dx, y + dy
                        x, y = i - dx, j - dy
                        while 0 <= x < board_size and 0 <= y < board_size and board[x][y] == player:
                            count += 1
                            x, y = x - dx, y - dy
                        if count >= 5:
                            return True
        return np.all(board != 0)                                                             # 因为怕输，所以全点了防守（bushi）