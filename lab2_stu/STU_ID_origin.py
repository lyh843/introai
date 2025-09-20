import numpy as np
import agent


# 超参数
# 每次拓展节点的深度
LEVEL = 4
# 下棋时考虑的距离有棋区域的范围
DIST = 1
#
NUM = 10
# 下棋的评分
# score = {"RUSH_FOUR": 100,
#          "LIVE_THREE": 100,
#          "Jump_THREE": 75,
#          "RUSH_THREE": 50,
#          "LIVE_TWO": 25,
#          "DEATH_TWO": 10,
#         }

class Search(agent.Agent):
    def __init__(self, player):
        super().__init__(player)
    def make_move(self, board):
        """
        Args:
            board: 接受一个棋盘作为输入
            
        Return: 
            返回一个元组(x, y)，代表下棋位置
        """        
        if (board == 0).all():
            return (len(board) // 2, len(board) // 2)
        
        check_loc = self.check_priority_moves(board)
        if check_loc:
            return check_loc
        
        area = self.search_area(board)
        up, down, left, right = area[0], area[1], area[2], area[3]
        value = float('-inf')
        result_loc = (0, 0)
        record = []
        for i in range(up, down + 1, 1):
            for j in range(left, right + 1):
                if board[i][j] != 0 : continue
                temp_score = self.judge_count(board, (i, j), self.player)
                record.append((temp_score, (i, j)))
        
        record.sort(reverse=True, key=lambda x: x[0])
        record = record[:NUM]
                
        for _, (i, j) in record:
            new_board = board.copy()                
            new_board[i][j] = self.player
            temp = self.maxmin(new_board, False, self.update_area(board, area, (i, j)), 0)
            if temp > value:
                value = temp
                result_loc = (i, j)
        
        return result_loc
                
    def evaluate(self, board):
        """
        传入当前的棋盘,
        计算一个评价数值。
        """
        board_size = len(board)
        value = 0        
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == self.player:
                    value += self.judge_count(board, (i, j), self.player)
                elif board[i][j] == self.opponent:
                    value -= 100 * self.judge_count(board, (i, j), self.opponent)
        
        return value
                                
    def maxmin(self, board, to_max, area, level = 0, alpha = float('-inf'), beta = float('inf')):
        """
        进行极大极小值判断以及剪枝处理。
        返回当前节点的value
        Args:
            board (_type_): _description_
            to_max (bool): 目前是否为极大值模型
        """
        if level == LEVEL:
            return self.evaluate(board)
        up, down, left, right = area
        new_board = board.copy()
        value = 0
        record = []
        if to_max:
            value = float('-inf')
            for i in range(up, down + 1, 1) :
                for j in range(left, right + 1, 1):
                    if board[i][j] != 0 : continue
                    score = self.judge_count(board, (i, j), self.player)
                    record.append((score, (i, j)))
            
            record.sort(reverse=True, key=lambda x: x[0])
            record = record[:NUM]
            
            for _, (i, j) in record:                    
                new_board[i][j] = self.player
                temp = self.maxmin(new_board, False, self.update_area(board, area, (i, j)), level + 1, alpha, beta)
                if temp > value:
                    value = temp
                    alpha = value
        else:
            value = float('inf')
            for i in range(up, down + 1, 1):
                for j in range(left, right + 1, 1):
                    if board[i][j] != 0: continue
                    score = self.judge_count(board, (i, j), self.opponent)
                    record.append((score, (i, j)))
                    
            record.sort(reverse=True, key= lambda x : x[0])
            record = record[:NUM]
            
            for _, (i, j) in record:        
                new_board[i][j] = self.opponent
                temp = self.maxmin(new_board, True, self.update_area(board, area, (i, j)), level + 1, alpha, beta)
                if temp < value:
                    value = temp
                    beta = value
                        
        return value
        
    def search_area(self, board):
        """返回maxmin搜索时遍历的节点

        Args:
            board (_type_): _description_
        """
        area = []
        up = down = left = right = False
        board_size = len(board)
        for i in range(board_size):
            if up : break
            for j in range(board_size):
                if board[i][j] != 0:
                    up = True
                    area.append(max(0, i - DIST))
                    break
        
        for i in range(board_size - 1, -1, - 1):
            if down : break
            for j in range(board_size):
                if board[i][j] != 0:
                    down = True
                    area.append(min(i + DIST, board_size - 1))
                    break
        
        for j in range(board_size):
            if left : break
            for i in range(board_size):
                if board[i][j] != 0:
                    left = True
                    area.append(max(0, j - DIST))
                    break
                
        for j in range(board_size - 1, -1, -1):
            if right : break
            for i in range(board_size):
                if board[i][j] != 0:
                    right = True
                    area.append(min(j + DIST, board_size - 1))
                    break
                
        return area
    
    def update_area(self, board, area, loc):
        new_area = area.copy()
        if loc[0] - DIST < area[0]:
            new_area[0] = max(loc[0] - DIST, 0)
        if loc[0] + DIST > area[1]:
            new_area[1] = min(loc[0] + DIST, len(board) - 1)
        if loc[1] - DIST < area[2]:
            new_area[2] = max(loc[1] - DIST, 0)
        if loc[1] + DIST > area[3]:
            new_area[3] = min(loc[1] + DIST, len(board) - 1)
        
        return new_area
    
    def judge_count(self, board, loc, target):
        x, y = loc
        board_size = len(board)
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]
        for dx, dy in directions:
            count_tar = 1
            count_space = 0
            count_barrier = 0
            # 正向
            for i in range(4):
                new_x, new_y = x + dx * (i + 1), y + dy * (i + 1)
                if 0 <= new_x < board_size and 0 <= new_y < board_size:
                    if board[new_x][new_y] == target:
                        count_tar += 1
                    elif board[new_x][new_y] == 0:
                        count_space += 1
                    else:
                        count_barrier += 1
                        break
                else:
                    count_barrier += 1
                    break
                
            # 反向
            for i in range(4):
                new_x, new_y = x - dx * (i + 1), y - dy * (i + 1)
                if 0 <= new_x < board_size and 0 <= new_y < board_size:
                    if board[new_x][new_y] == target:
                        count_tar += 1
                    elif board[new_x][new_y] == 0:
                        count_space += 1
                    else:
                        count_barrier += 1
                        break
                else:
                    count_barrier += 1
                    break
            
            if count_tar >= 5:
                return 50000
            elif count_tar == 4 and count_space >= 1:
                return 50000
            elif count_tar == 3 and count_space >= 2:
                return 3000
            elif count_tar == 2 and count_space >= 3:
                return 50
            elif count_tar == 1:
                return 5
            elif count_tar == 3 and count_space == 1:
                return 200
            elif count_tar == 3:
                return 60
            elif count_tar == 2:
                return 30
        
        return 0
    
    def check_priority_moves(self, board):
        """
        检查是否有优先级很高的着法，如：
        1. 自己可以获胜的点（活四）
        2. 对手即将获胜需要阻止的点（对手的活四或冲四）
        3. 自己可以形成活四的点
        """
        board_size = len(board)
        # 检查自己是否有获胜点（可以直接形成五子）
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == 0:
                    # 检查自己在此处落子是否能获胜
                    board[i][j] = self.player
                    if self.judge_count(board, (i, j), self.player) >= 100000:
                        board[i][j] = 0  # 恢复棋盘
                        return (i, j)
                    board[i][j] = 0  # 恢复棋盘
        
        # 检查对手是否有即将获胜的点，需要阻止
        threat_moves = []  # 存储对手的威胁点
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == 0:
                    # 检查对手在此处落子的威胁程度
                    board[i][j] = self.opponent
                    score = self.judge_count(board, (i, j), self.opponent)
                    if score >= 50000:  # 对手可以获胜
                        board[i][j] = 0
                        return (i, j)  # 立即阻止
                    elif score >= 10000:  # 对手有冲四等威胁
                        threat_moves.append((score, (i, j)))
                    board[i][j] = 0
        
        # 如果有威胁点，返回威胁最大的点
        if threat_moves:
            threat_moves.sort(reverse=True)
            return threat_moves[0][1]
        
        # 检查自己是否有形成活四的点
        good_moves = []
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == 0:
                    board[i][j] = self.player
                    score = self.judge_count(board, (i, j), self.player)
                    if score >= 50000:  # 自己可以形成活四
                        good_moves.append((score, (i, j)))
                    board[i][j] = 0
        
        if good_moves:
            good_moves.sort(reverse=True)
            return good_moves[0][1]
        
        return None  # 没有优先级很高的着法