import numpy as np
import agent
import hashlib

# 超参数
LEVEL = 4  # 搜索深度
NUM = 15   # 每层尝试的候选点数量
DIST = 2   # 搜索范围距离
W = 10     # 防守/进攻权重比

# 棋型评分
scores = [0, 1, 10, 1000, 10000, 100000000]

class Search(agent.Agent):
    def __init__(self, player):
        super().__init__(player)
        self.board_size = None  # 动态设置
        self.directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        self.cache = {}
        
        # 移动方向（与第一个代码相同）
        self.moves = [(-1, -1), (-1, 0), (0, -1), (-1, 1)]
        self.coe = [-2, 1]  # 对手和AI的系数
        
        # 延迟初始化，等待知道棋盘大小
        self.map = None
        self.score_queue = None
        self.set_num = 0
        self.total_score = 0
        
    def initialize_board(self, board_size):
        """根据实际棋盘大小初始化数据结构"""
        self.board_size = board_size
        self.map = [[{
            'set': 0,  # 0:空, 1:AI, 2:对手
            'score': 0,
            'info': [[0, 0, 0, 0] for _ in range(4)]  # 四个方向的棋型信息
        } for _ in range(board_size)] for _ in range(board_size)]
        
        self.set_num = 0
        self.total_score = 0
        self.score_queue = []
        
        # 初始化候选队列
        for i in range(board_size):
            for j in range(board_size):
                self.score_queue.append((i, j, 0))
        
    def make_move(self, board):
        """主决策函数"""
        board_size = len(board)
        
        # 如果是第一次调用或者棋盘大小变化，重新初始化
        if self.board_size != board_size or self.map is None:
            self.initialize_board(board_size)
        
        if (board == 0).all():
            center = board_size // 2
            return (center, center)
        
        # 同步外部棋盘状态到内部数据结构
        self.sync_board(board)
        
        # 清空缓存并开始搜索
        self.cache = {}
        best_move, _ = self.negamax_search(LEVEL, -float('inf'), float('inf'))
        
        return best_move

    def sync_board(self, board):
        """将numpy棋盘同步到内部数据结构"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                current_set = self.map[i][j]['set']
                board_val = board[i][j]
                
                if board_val != 0 and current_set == 0:
                    # 新增棋子
                    color = 1 if board_val == self.player else 0
                    self.update_map(i, j, color, False)
                elif board_val == 0 and current_set != 0:
                    # 移除棋子
                    color = current_set - 1
                    self.update_map(i, j, color, True)

    def update_map(self, r, c, num, remove):
        """核心更新函数"""
        moves = self.moves
        coe = self.coe
        
        if not remove:
            self.map[r][c]['set'] = num + 1
            self.set_num += 1
        else:
            self.map[r][c]['set'] = 0
            self.set_num -= 1
        
        changes = 0
        
        # 更新四个方向
        for i in range(4):
            dx, dy = moves[i]
            x, y = r, c
            step = 5
            
            while step > 0 and 0 <= x < self.board_size and 0 <= y < self.board_size:
                # 检查边界
                xx = x - dx * 4
                yy = y - dy * 4
                if xx >= self.board_size or yy < 0 or yy >= self.board_size:
                    x += dx
                    y += dy
                    step -= 1
                    continue
                
                cur_info = self.map[x][y]['info'][i]
                
                if not remove:
                    # 新增棋子
                    if cur_info[2] > 0:
                        s = scores[cur_info[2]]
                        changes -= s * cur_info[3]
                        self.update_score_along_line(x, y, dx, dy, 5, -s)
                    
                    cur_info[num] += 1
                    
                    if cur_info[1 - num] > 0:
                        cur_info[2] = 0
                    else:
                        cur_info[2] = cur_info[num]
                        cur_info[3] = coe[num]
                        s = scores[cur_info[2]]
                        changes += s * cur_info[3]
                        self.update_score_along_line(x, y, dx, dy, 5, s)
                
                else:
                    # 移除棋子
                    if cur_info[2] > 0:
                        s = scores[cur_info[2]]
                        changes -= s * cur_info[3]
                        self.update_score_along_line(x, y, dx, dy, 5, -s)
                        cur_info[2] -= 1
                    
                    cur_info[num] -= 1
                    
                    sc = 0
                    if cur_info[num] > 0:
                        sc = 1
                    elif cur_info[1 - num] > 0 and cur_info[num] == 0:
                        sc = -1
                    
                    if sc == 1:
                        cur_info[2] = cur_info[num]
                        s = scores[cur_info[2]]
                        changes += s * cur_info[3]
                        self.update_score_along_line(x, y, dx, dy, 5, s)
                    elif sc == -1:
                        cur_info[2] = cur_info[1 - num]
                        cur_info[3] = coe[1 - num]
                        s = scores[cur_info[2]]
                        changes += s * cur_info[3]
                        self.update_score_along_line(x, y, dx, dy, 5, s)
                
                x += dx
                y += dy
                step -= 1
        
        self.total_score += changes
        self.sort_candidates()

    def update_score_along_line(self, x, y, dx, dy, steps, delta):
        """沿直线更新评分"""
        for _ in range(steps):
            if 0 <= x < self.board_size and 0 <= y < self.board_size:
                self.map[x][y]['score'] += delta
                x -= dx
                y -= dy

    def sort_candidates(self):
        """排序候选落子点"""
        self.score_queue = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.map[i][j]['set'] == 0:
                    self.score_queue.append((i, j, self.map[i][j]['score']))
        
        self.score_queue.sort(key=lambda x: x[2], reverse=True)

    def simulate_move(self, r, c, num):
        """模拟落子"""
        self.update_map(r, c, num, False)

    def undo_move(self, r, c, num):
        """撤销落子"""
        self.update_map(r, c, num, True)

    def get_candidates(self, num, count=NUM):
        """获取候选落子点"""
        candidates = []
        for i, j, score in self.score_queue:
            if self.map[i][j]['set'] == 0:
                candidates.append((score, i, j))
                if len(candidates) >= count:
                    break
        return candidates

    def negamax_search(self, depth, alpha, beta):
        """负极大值搜索主函数"""
        if depth == 0:
            return None, self.evaluate_board()
        
        # 检查缓存
        board_hash = self.get_board_hash()
        if board_hash in self.cache:
            return self.cache[board_hash]
        
        best_move = None
        best_score = -float('inf')
        
        # 获取候选点
        current_player = 1 if (LEVEL - depth) % 2 == 0 else 0
        candidates = self.get_candidates(current_player, min(NUM, len(self.score_queue)))
        
        for score, i, j in candidates:
            self.simulate_move(i, j, current_player)
            
            # 递归搜索
            _, child_score = self.negamax_search(depth - 1, -beta, -alpha)
            child_score = -child_score
            
            self.undo_move(i, j, current_player)
            
            if child_score > best_score:
                best_score = child_score
                best_move = (i, j)
                alpha = max(alpha, best_score)
            
            if alpha >= beta:
                break
        
        result = (best_move, best_score)
        self.cache[board_hash] = result
        return result

    def evaluate_board(self):
        """评估棋盘状态"""
        return self.total_score

    def get_board_hash(self):
        """生成棋盘状态的哈希值"""
        hash_str = ""
        for i in range(self.board_size):
            for j in range(self.board_size):
                hash_str += str(self.map[i][j]['set'])
                for dir_info in self.map[i][j]['info']:
                    hash_str += "".join(map(str, dir_info))
        
        return hashlib.md5(hash_str.encode()).hexdigest()

    def in_board(self, loc):
        """检查位置是否在棋盘内"""
        i, j = loc
        return (0 <= i < self.board_size) and (0 <= j < self.board_size)

    def search_area(self):
        """搜索范围（备用方法）"""
        min_i = min_j = self.board_size
        max_i = max_j = 0
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.map[i][j]['set'] != 0:
                    min_i = min(min_i, max(0, i - DIST))
                    min_j = min(min_j, max(0, j - DIST))
                    max_i = max(max_i, min(self.board_size - 1, i + DIST))
                    max_j = max(max_j, min(self.board_size - 1, j + DIST))
        
        # 如果没有棋子，返回整个棋盘
        if min_i == self.board_size:
            return 0, self.board_size - 1, 0, self.board_size - 1
        
        return min_i, max_i, min_j, max_j
