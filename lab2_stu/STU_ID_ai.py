import numpy as np
import agent

LEVEL = 3
DIST = 1
W = 10
DIRE = [(0, 1), (0, -1), (1, 0),(-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1)]
scores = {"Five":100000,
          "LIVE_FOUR":100000,
          "DEATH_FOUR":50000,
          "LIVE_THREE":5000,
          "SLEEP_THREE":1000,
          "LIVE_TWO":100}

class Search(agent.Agent):
    def __init__(self, player):
        super().__init__(player)

    def make_move(self, board):
        if (board == 0).all():
            return (len(board) // 2, len(board) // 2)
        
        # 初始化分数表
        self.score_player, self.score_opponent = self.init_scores(board)

        area = self.search_area(board)
        value = float('-inf')
        result_loc = (0, 0)
        record = []

        for point in area:
            i, j = point
            if board[i][j] != 0: 
                continue
            temp_score = self.judge_count(board, (i, j), self.player)
            record.append((temp_score, (i, j)))
        
        record.sort(reverse=True, key=lambda x: x[0])
                
        for _, (i, j) in record:              
            board[i][j] = self.player
            # 增量更新
            backup_p, backup_o = self.score_player.copy(), self.score_opponent.copy()
            self.update_scores(board, i, j)
            temp = self.maxmin(board, False, self.search_area(board), 0)
            # 回溯
            self.score_player, self.score_opponent = backup_p, backup_o
            board[i][j] = 0
            if temp > value:
                value = temp
                result_loc = (i, j)
        
        return result_loc
    
    # 初始化分数表
    def init_scores(self, board):
        score_player = np.zeros_like(board, dtype=int)
        score_opponent = np.zeros_like(board, dtype=int)
        n = len(board)
        for i in range(n):
            for j in range(n):
                if board[i][j] == 0:
                    score_player[i][j] = self.judge_count(board, (i,j), self.player)
                    score_opponent[i][j] = self.judge_count(board, (i,j), self.opponent)
        return score_player, score_opponent

    # 落子后更新局部分数
    def update_scores(self, board, x, y):
        rng = 5
        n = len(board)
        for i in range(max(0, x-rng), min(n, x+rng+1)):
            for j in range(max(0, y-rng), min(n, y+rng+1)):
                if board[i][j] == 0:
                    self.score_player[i][j] = self.judge_count(board, (i,j), self.player)
                    self.score_opponent[i][j] = self.judge_count(board, (i,j), self.opponent)
                else:
                    self.score_player[i][j] = 0
                    self.score_opponent[i][j] = 0

    def evaluate(self, board):
        return np.sum(self.score_player) - W * np.sum(self.score_opponent)

    def maxmin(self, board, to_max, area, level=0, alpha=float('-inf'), beta=float('inf')):
        if level == LEVEL or self.check_win(board):
            return self.evaluate(board)
        
        record = []
        if to_max:
            value = float('-inf')
            for point in area:
                i, j = point
                if board[i][j] != 0: continue
                score = self.judge_count(board, (i, j), self.player)
                record.append((score, (i, j)))
            record.sort(reverse=True, key=lambda x: x[0])

            for _, (i, j) in record:                    
                board[i][j] = self.player
                backup_p, backup_o = self.score_player.copy(), self.score_opponent.copy()
                self.update_scores(board, i, j)
                temp = self.maxmin(board, False, self.search_area(board), level+1, alpha, beta)
                self.score_player, self.score_opponent = backup_p, backup_o
                board[i][j] = 0
                if temp > value:
                    value = temp
                    alpha = max(value, alpha)
                if beta <= alpha:
                    break
        else:
            value = float('inf')
            for point in area:
                i, j = point
                if board[i][j] != 0: continue
                score = self.judge_count(board, (i, j), self.opponent)
                record.append((score, (i, j)))
            record.sort(reverse=True, key=lambda x: x[0])

            for _, (i, j) in record:        
                board[i][j] = self.opponent
                backup_p, backup_o = self.score_player.copy(), self.score_opponent.copy()
                self.update_scores(board, i, j)
                temp = self.maxmin(board, True, self.search_area(board), level+1, alpha, beta)
                self.score_player, self.score_opponent = backup_p, backup_o
                board[i][j] = 0
                if temp < value:
                    value = temp
                    beta = min(value, beta)
                if beta <= alpha:
                    break
        return value
    
    def search_area(self, board):
        area = set()
        board_size = len(board)
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] != 0:
                    for dist in range(1, DIST+1):
                        for dx, dy in DIRE:
                            ni, nj = i + dx*dist, j + dy*dist
                            if 0 <= ni < board_size and 0 <= nj < board_size and board[ni][nj] == 0:
                                area.add((ni, nj))
        return area
    
    def judge_count(self, board, loc, target):
        x, y = loc
        board_size = len(board)
        max_score = 0
        
        for dx, dy in DIRE:
            count = 1
            empty = 0
            for i in range(6):
                new_x, new_y = x + dx*i, y + dy*i
                if not (0 <= new_x < board_size and 0 <= new_y < board_size):
                    break
                if board[new_x][new_y] == target:
                    count += 1
                elif board[new_x][new_y] == 0:
                    empty += 1
                    break
                else:
                    break
            if count >= 5:
                max_score += scores["Five"]
            elif count == 4 and empty >= 2:
                max_score += scores["LIVE_FOUR"]
            elif count == 4 and empty >= 1:
                max_score += scores["DEATH_FOUR"]
            elif count == 3 and empty >= 2:
                max_score += scores["LIVE_THREE"]
            elif count == 3 and empty >= 1:
                max_score += scores["SLEEP_THREE"]
            elif count == 2 and empty >= 3:
                max_score += scores["LIVE_TWO"]
        return max_score
    
    def check_win(self, board):
        n = len(board)
        for i in range(n):
            for j in range(n):
                if board[i][j] != 0:
                    player = board[i][j]
                    for dx, dy in [(0,1),(1,0),(1,1),(1,-1)]:
                        count = 1
                        x, y = i+dx, j+dy
                        while 0 <= x < n and 0 <= y < n and board[x][y] == player:
                            count += 1
                            x, y = x+dx, y+dy
                        x, y = i-dx, j-dy
                        while 0 <= x < n and 0 <= y < n and board[x][y] == player:
                            count += 1
                            x, y = x-dx, y-dy
                        if count >= 5:
                            return True
        return False
