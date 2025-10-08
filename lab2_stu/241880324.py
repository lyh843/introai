import numpy as np
import agent


# 超参数
# 每次拓展节点的深度
LEVEL = 2
# 下棋时考虑的距离有棋区域的范围
DIST = 1
# 价值评估函数中，防守 / 进攻 的比值，默认为1
W1 = 1 # 进攻
W2 = 1.23 # 防守
# 方向
DIRE = [(0, 1), (0, -1), (1, 0),(-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1)]
# 评价分数
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
        """`
        Args:
            board: 接受一个棋盘作为输入
            
        Return: 
            返回一个元组(x, y)，代表下棋位置
        """
        # 如果棋盘为空，直接下在中间位置        
        if (board == 0).all():
            return (len(board) // 2, len(board) // 2)
        
        # 遍历要下的区域
        area = self.search_area(board)
        
        value = float('-inf')
        result_loc = (0, 0)
        record = []
        # 初次判断，直接判断这个节点的重要性
        for point in area:
            i, j = point
            if board[i][j] != 0 : continue
            temp_score = self.judge_count(board, (i, j), self.player)
            record.append((temp_score, (i, j)))
        
        record.sort(reverse=True, key=lambda x: x[0])
                
        for _, (i, j) in record:              
            board[i][j] = self.player
            temp = self.maxmin(board, False, self.search_area(board), 0)
            board[i][j] = 0
            if temp > value:
                value = temp
                result_loc = (i, j)
        
        return result_loc
                
    def evaluate(self, board, isPlayer: bool):
        """
        传入当前的棋盘,
        计算一个评价数值。
        返回一个对于player的得分
        """
        value = 0        
        board_size = len(board)
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == self.player:
                    player_score = self.judge_count(board, (i, j), self.player)
                    value += player_score
                elif board[i][j] == self.opponent:
                    if isPlayer: # 考虑这一步是谁下，来进行动态的权重分配
                        opponent_score = self.judge_count(board, (i, j), self.opponent) / W1
                    else:
                        opponent_score = W2 * self.judge_count(board, (i, j), self.opponent)
                    value -= opponent_score
                    
        return value
                                
    def maxmin(self, board, to_max: bool, area, level = 0, alpha = float('-inf'), beta = float('inf')):
        """
        进行极大极小值判断以及剪枝处理。
        返回当前节点的value
        Args:
            board (_type_): _description_
            to_max (bool): 目前是否为极大值模型
        """
        # 到达底部就返回
        if level == LEVEL or self.check_win(board):
            return self.evaluate(board, to_max)
        
        value = 0
        record = []
        if to_max:
            value = float('-inf')
            # 初步筛选
            for point in area:
                i, j = point
                if board[i][j] != 0 : continue
                score = self.judge_count(board, (i, j), self.player)
                record.append((score, (i, j)))
            
            record.sort(reverse=True, key=lambda x: x[0])
            
            for _, (i, j) in record:                    
                board[i][j] = self.player
                temp = self.maxmin(board, False, self.search_area(board), level + 1, alpha, beta)
                board[i][j] = 0
                if temp > value:
                    value = temp
                    alpha = max(value, alpha)
                if beta <= alpha:
                    break
                
        else:
            value = float('inf')
            # 初步筛选，选出前 NUM 个有价值的点
            for point in area:
                i, j = point
                if board[i][j] != 0: continue
                score = self.judge_count(board, (i, j), self.opponent)
                record.append((score, (i, j)))
                    
            record.sort(reverse=True, key= lambda x : x[0])
            
            for _, (i, j) in record:        
                board[i][j] = self.opponent
                temp = self.maxmin(board, True, self.search_area(board), level + 1, alpha, beta)
                board[i][j] = 0
                if temp < value:
                    value = temp
                    beta = min(value, beta)
                if beta <= alpha:
                    break
                        
        return value
        
    def search_area(self, board):
        """
            返回maxmin搜索时遍历的节点
            即有棋子区域的DIST范围区域内
        Args:
            board (_type_): _description_
        """
        area = set()
        board_size = len(board)
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] != 0:
                    for dist in range(1, DIST + 1):
                        for dx, dy in DIRE:
                            if 0 <= i + dx * dist < board_size and 0 <= j + dy * dist < board_size and board[i + dx * dist][j + dy * dist] == 0:
                                area.add((i + dx * dist, j + dy * dist))

        return area
    
    def judge_count(self, board, loc, target):
        x, y = loc
        board_size = len(board)
        
        max_score = 0
        
        for dx, dy in DIRE:
            count = 1  # 包含当前位置
            blocked = 0
            empty = 0
            
            for i in range(6):
                new_x, new_y = x + dx * i, y + dy * i
                if not (0 <= new_x < board_size and 0 <= new_y < board_size):
                    blocked += 1
                    break
                if board[new_x][new_y] == target:
                    count += 1
                elif board[new_x][new_y] == 0:
                    empty += 1
                    break
                else:
                    blocked += 1
                    break
            
            # 更准确的评分逻辑
            if count >= 5:
                max_score += scores["Five"]  # 成五
            elif count == 4 and empty >= 2:
                max_score += scores["LIVE_FOUR"]   # 活四
            elif count == 4 and empty >= 1:
                max_score += scores["DEATH_FOUR"]   # 冲四
            elif count == 3 and empty >= 2:
                max_score += scores["LIVE_THREE"] # 活三
            elif count == 3 and empty >= 1:
                max_score += scores["SLEEP_THREE"]  # 眠三
            elif count == 2 and empty >= 3:
                max_score += scores["LIVE_TWO"]   # 活二
        
        return max_score
    
    def check_win(self, board):
        """
        检查从指定位置是否形成五子连珠

        @param board: 棋盘
        @param row: 最后落子的行坐标
        @param col: 最后落子的列坐标
        @return: 是否获胜
        """
        board_size = len(board)
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] != 0:
                    player = board[i][j]
                    directions = [
                        (0, 1),
                        (1, 0),
                        (1, 1),
                        (1, -1),
                    ]

                    for dx, dy in directions:
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
        return False