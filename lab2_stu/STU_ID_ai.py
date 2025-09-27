import numpy as np
import agent


# 超参数
# 每次拓展节点的深度
LEVEL = 3
# 下棋时考虑的距离有棋区域的范围
DIST = 2
#
NUM = 5
# 价值评估函数中，防守 / 进攻 的比值，默认为1
W = 1000000
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
        """改进的下棋逻辑，优先防守"""
        if (board == 0).all():
            return (len(board) // 2, len(board) // 2)
        
        area = self.search_area(board)
        
        # 第一步：检查紧急情况
        urgent_move = self.check_urgent_moves(board, area)
        if urgent_move and isinstance(urgent_move, tuple):
            return urgent_move
        
        # 第二步：评估候选位置
        candidates = self.get_candidate_moves(board, area)
        
        best_score = float('-inf')
        best_move = candidates[0] if candidates else (len(board)//2, len(board)//2)
        
        for move in candidates[:NUM]:  # 只评估前NUM个候选
            i, j = move
            board[i][j] = self.player
            score = self.maxmin(board, True, self.update_area(board, area, move), 0)
            board[i][j] = 0
            
            # 给防守性走法额外加分
            if self.is_defensive_move(board, move):
                score += 1000  # 防守奖励
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

    def is_defensive_move(self, board, move):
        """判断是否是防守性走法"""
        i, j = move
        # 检查是否在对手棋子附近
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx == 0 and dy == 0:
                    continue
                ni, nj = i + dx, j + dy
                if 0 <= ni < len(board) and 0 <= nj < len(board):
                    if board[ni][nj] == self.opponent:
                        return True
        return False
                
    def evaluate(self, board, area):
        """平衡攻防的评估函数"""
        player_score = 0
        opponent_score = 0
        
        # 首先检查是否有立即胜利或需要立即防守的情况
        urgent_move = self.check_urgent_moves(board, area)
        if urgent_move:
            return urgent_move
        
        # 评估每个重要位置
        important_positions = self.get_important_positions(board, area)
        
        for pos in important_positions:
            i, j = pos
            if board[i][j] == 0:
                # 进攻价值：我方能形成的棋型
                player_attack = self.evaluate_position(board, (i, j), self.player)
                # 防守价值：阻止对方形成的棋型
                player_defense = self.evaluate_position(board, (i, j), self.opponent)
                
                # 对手的威胁
                opponent_attack = self.evaluate_position(board, (i, j), self.opponent)
                opponent_defense = self.evaluate_position(board, (i, j), self.player)
                
                # 综合评分：既要考虑进攻也要考虑防守
                player_score += player_attack + player_defense * 1.5  # 防守更重要
                opponent_score += opponent_attack + opponent_defense
        
        return player_score - opponent_score * 1.2  # 更重视防守对手

    def check_urgent_moves(self, board, area):
        """检查紧急情况：立即胜利或必须防守的棋型"""
        urgent_positions = []
        
        # 检查我方是否能立即获胜
        win_move = self.find_winning_move(board, self.player, area)
        if win_move:
            return 1000000  # 极大值，确保选择这个位置
        
        # 检查对手是否能立即获胜（必须防守）
        opponent_win_move = self.find_winning_move(board, self.opponent, area)
        if opponent_win_move:
            return -800000  # 必须防守的极大负值
        
        # 检查对手的活四、冲四等威胁
        threat_moves = self.find_threat_moves(board, self.opponent, area)
        if threat_moves:
            return -500000  # 高威胁需要防守
        
        return None

    def find_winning_move(self, board, player, area):
        """寻找能立即获胜的位置"""
        for i in range(area[0], area[1] + 1):
            for j in range(area[2], area[3] + 1):
                if board[i][j] == 0:
                    board[i][j] = player
                    if self.is_win(board, player, (i, j)):
                        board[i][j] = 0
                        return (i, j)
                    board[i][j] = 0
        return None

    def find_threat_moves(self, board, player, area):
        """寻找威胁位置：活四、冲四、双活三等"""
        threat_positions = []
        
        for i in range(area[0], area[1] + 1):
            for j in range(area[2], area[3] + 1):
                if board[i][j] == 0:
                    # 模拟下棋
                    board[i][j] = player
                    threat_level = self.evaluate_threat_level(board, player, (i, j))
                    board[i][j] = 0
                    
                    if threat_level >= 3:  # 活四、冲四等级别
                        threat_positions.append((i, j))
        
        return threat_positions if threat_positions else None
    
    def evaluate_position(self, board, pos, player):
        """更准确的棋型评估"""
        x, y = pos
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        total_score = 0
        
        for dx, dy in directions:
            score = self.evaluate_direction(board, x, y, dx, dy, player)
            total_score += score
        
        return total_score

    def evaluate_direction(self, board, x, y, dx, dy, player):
        """单个方向的棋型评估"""
        board_size = len(board)
        
        # 统计连续棋子数量
        count = 1  # 当前位置
        
        # 正向统计
        blocked_front = False
        for i in range(1, 6):
            nx, ny = x + dx * i, y + dy * i
            if not (0 <= nx < board_size and 0 <= ny < board_size):
                blocked_front = True
                break
            if board[nx][ny] == player:
                count += 1
            else:
                if board[nx][ny] != 0:
                    blocked_front = True
                break
        
        # 反向统计
        blocked_back = False
        for i in range(1, 6):
            nx, ny = x - dx * i, y - dy * i
            if not (0 <= nx < board_size and 0 <= ny < board_size):
                blocked_back = True
                break
            if board[nx][ny] == player:
                count += 1
            else:
                if board[nx][ny] != 0:
                    blocked_back = True
                break
        
        # 评估棋型
        return self.assess_pattern(count, blocked_front, blocked_back)

    def assess_pattern(self, count, blocked_front, blocked_back):
        """根据连续数量和阻塞情况评估棋型"""
        if count >= 5:
            return scores["Five"]
        
        blocked_count = (1 if blocked_front else 0) + (1 if blocked_back else 0)
        
        if blocked_count == 0:  # 活棋
            if count == 4:
                return scores["LIVE_FOUR"]
            elif count == 3:
                return scores["LIVE_THREE"]
            elif count == 2:
                return scores["LIVE_TWO"]
        elif blocked_count == 1:  # 半活棋
            if count == 4:
                return scores["DEATH_FOUR"]
            elif count == 3:
                return scores["SLEEP_THREE"]
        
        return 0
    def has_neighbor(self, board, pos, distance):
        """检查位置周围是否有棋子"""
        x, y = pos
        board_size = len(board)
        for dx in range(-distance, distance + 1):
            for dy in range(-distance, distance + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < board_size and 0 <= ny < board_size:
                    if board[nx][ny] != 0:
                        return True
        return False
                                
    def maxmin(self, board, to_max, area, level = 0, alpha = float('-inf'), beta = float('inf')):
        """
        进行极大极小值判断以及剪枝处理。
        返回当前节点的value
        Args:
            board (_type_): _description_
            to_max (bool): 目前是否为极大值模型
        """
        # 到达底部就返回
        if level == LEVEL:
            return self.evaluate(board, area)
        
        up, down, left, right = area
        value = 0
        record = []
        if to_max:
            value = float('-inf')
            # 初步筛选，选出前 NUM 个有价值的点
            for i in range(up, down + 1, 1) :
                for j in range(left, right + 1, 1):
                    if board[i][j] != 0 : continue
                    score = self.judge_count(board, (i, j), self.player)
                    if score >= scores["Five"]: # 已经定输赢了，不需要再次深入
                        return float('inf')
                    record.append((score, (i, j)))
            
            record.sort(reverse=True, key=lambda x: x[0])
            record = record[:NUM]
            
            for _, (i, j) in record:                    
                board[i][j] = self.player
                temp = self.maxmin(board, False, self.update_area(board, area, (i, j)), level + 1, alpha, beta)
                board[i][j] = 0
                if temp > value:
                    value = temp
                    alpha = max(value, alpha)
                if beta <= alpha:
                    break
                
        else:
            value = float('inf')
            # 初步筛选，选出前 NUM 个有价值的点
            for i in range(up, down + 1, 1):
                for j in range(left, right + 1, 1):
                    if board[i][j] != 0: continue
                    score = self.judge_count(board, (i, j), self.opponent)
                    if score >= scores["Five"]:
                        return - W * scores["Five"]
                    record.append((score, (i, j)))
                    
            record.sort(reverse=True, key= lambda x : x[0])
            record = record[:NUM]
            
            for _, (i, j) in record:        
                board[i][j] = self.opponent
                temp = self.maxmin(board, True, self.update_area(board, area, (i, j)), level + 1, alpha, beta)
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
            返回的实质是一个正方形区域，包含所有需要遍历的节点
            up, left 是小数字
            down, right 是大数字

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
            (0, -1),
            (-1, 0),
            (-1, -1),
            (-1, 1)
        ]
        
        max_score = 0
        
        for dx, dy in directions:
            count = 1  # 包含当前位置
            blocked = 0
            empty = 0
            
            for i in range(1, 5):
                new_x, new_y = x + dx * i, y + dy * i
                if not (0 <= new_x < board_size and 0 <= new_y < board_size):
                    blocked += 1
                    break
                if board[new_x][new_y] == target:
                    count += 1
                elif board[new_x][new_y] == 0:
                    empty += 1
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