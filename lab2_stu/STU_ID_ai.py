import numpy as np
from collections import deque
from agent import Agent


class Search(Agent):
    """基于JavaScript专家难度算法的五子棋AI，专为11×11棋盘优化"""
    
    def __init__(self, player):
        super().__init__(player)
        self.board_size = 11
        self.initialize_ai()
        
    def initialize_ai(self):
        """初始化AI参数和数据结构"""
        # 专家难度参数
        self.depth = 7
        self.totry = [10, 10]
        
        # 评分系统
        self.scores = [0, 1, 10, 2000, 4000, 100000000000]
        self.coe = [-2, 1]  # 对手和己方的系数
        
        # 四个评估方向
        self.directions = [(-1, -1), (-1, 0), (0, -1), (-1, 1)]
        
        # 状态变量
        self.total_score = 0
        self.pieces_count = 0
        self.cache = {}
        
        # 初始化棋盘数据结构
        self.initialize_board()
    
    class BoardPoint:
        """棋盘格子数据结构"""
        def __init__(self, row, col):
            self.row = row
            self.col = col
            self.has_piece = False
            self.score = 0
            # 四个方向的信息: [己方数量, 对方数量, 当前状态, 系数]
            self.direction_info = [[0, 0, 0, 0] for _ in range(4)]
        
        def __lt__(self, other):
            """用于排序，分数高的优先"""
            if self.has_piece:
                return False
            if other.has_piece:
                return True
            return self.score > other.score
    
    def initialize_board(self):
        """初始化棋盘数据结构"""
        self.board = []
        self.score_queue = deque()
        
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                point = self.BoardPoint(i, j)
                row.append(point)
                self.score_queue.append(point)
            self.board.append(row)
        
        # 棋盘状态数组
        self.board_state = np.zeros((self.board_size, self.board_size), dtype=np.uint8)
    
    def make_move(self, board):
        """
        主决策函数，返回最佳移动位置
        """
        # 同步外部棋盘状态
        self.sync_board_state(board)
        
        # 清空缓存
        self.cache = {}
        
        # 如果没有空位，返回None
        if self.pieces_count >= self.board_size * self.board_size:
            return None
        
        # 使用负极大值算法搜索最佳移动
        alpha = float('-inf')
        best_move = None
        
        # 获取候选移动并按评分排序
        candidate_moves = self.get_candidate_moves()
        
        # 评估每个候选移动
        for move in candidate_moves[:self.totry[0]]:
            row, col = move
            score = -self.negamax_search(row, col, self.depth, float('-inf'), -alpha)
            self.undo_move(row, col, self.depth % 2)
            
            if score > alpha:
                alpha = score
                best_move = (row, col)
        
        return best_move if best_move else candidate_moves[0]
    
    def sync_board_state(self, external_board):
        """同步外部棋盘状态到内部数据结构"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                external_val = external_board[i][j]
                internal_point = self.board[i][j]
                
                if external_val == 0 and internal_point.has_piece:
                    # 移除棋子
                    self.update_board(i, j, 'remove')
                elif external_val == self.player and not internal_point.has_piece:
                    # 放置己方棋子
                    self.update_board(i, j, self.player)
                elif external_val == self.opponent and not internal_point.has_piece:
                    # 放置对方棋子
                    self.update_board(i, j, self.opponent)
    
    def update_board(self, row, col, action):
        """更新棋盘状态"""
        if action == 'remove':
            piece_type = self.board[row][col].has_piece - 1
            self._update_internal_board(row, col, piece_type, True)
            self.pieces_count -= 1
        else:
            piece_type = 1 if action == self.player else 0
            self._update_internal_board(row, col, piece_type, False)
            self.pieces_count += 1
    
    def _update_internal_board(self, row, col, piece_type, is_remove):
        """内部棋盘更新逻辑"""
        score_change = 0
        
        for dir_idx, (dr, dc) in enumerate(self.directions):
            r, c = row, col
            
            for step in range(5):
                if not (0 <= r < self.board_size and 0 <= c < self.board_size):
                    break
                
                point = self.board[r][c]
                dir_info = point.direction_info[dir_idx]
                
                if not is_remove:
                    # 放置棋子
                    if dir_info[2] > 0:
                        score_change -= self._update_direction_score(r, c, dir_idx, -dir_info[3])
                    
                    dir_info[piece_type] += 1
                    
                    if dir_info[1 - piece_type] > 0:
                        dir_info[2] = 0
                    else:
                        dir_info[2] = dir_info[piece_type]
                        dir_info[3] = self.coe[piece_type]
                        score_change += self._update_direction_score(r, c, dir_idx, dir_info[3])
                
                else:
                    # 移除棋子 - 简化实现
                    if dir_info[2] > 0:
                        score_change -= self._update_direction_score(r, c, dir_idx, -dir_info[3])
                    dir_info[piece_type] -= 1
                    # 这里需要更复杂的移除逻辑...
                
                r += dr
                c += dc
        
        self.total_score += score_change
    
    def _update_direction_score(self, row, col, direction, multiplier):
        """更新某个方向的分数"""
        dr, dc = self.directions[direction]
        point = self.board[row][col]
        dir_info = point.direction_info[direction]
        score_value = self.scores[dir_info[2]]
        
        total_change = 0
        r, c = row, col
        
        for step in range(5):
            if 0 <= r < self.board_size and 0 <= c < self.board_size:
                change = score_value * multiplier
                self.board[r][c].score += change
                total_change += change
                r -= dr
                c -= dc
        
        return total_change
    
    def simulate_move(self, row, col, piece_type):
        """模拟落子"""
        self.pieces_count += 1
        self._update_internal_board(row, col, piece_type, False)
    
    def undo_move(self, row, col, piece_type):
        """撤销模拟落子"""
        self._update_internal_board(row, col, piece_type, True)
        self.pieces_count -= 1
    
    def negamax_search(self, row, col, depth, alpha, beta):
        """负极大值搜索算法"""
        self.simulate_move(row, col, depth % 2)
        
        # 检查胜利条件
        if abs(self.total_score) >= 10000000:
            result = float('-inf')
            self.undo_move(row, col, depth % 2)
            return result
        
        # 棋盘已满
        if self.pieces_count >= self.board_size * self.board_size:
            result = 0
            self.undo_move(row, col, depth % 2)
            return result
        
        # 达到搜索深度
        if depth == 0:
            result = self.total_score
            self.undo_move(row, col, depth % 2)
            return result
        
        # 获取候选移动
        candidate_moves = self.get_candidate_moves()
        best_score = float('-inf')
        
        # 评估候选移动
        for move in candidate_moves[:self.totry[depth % 2]]:
            move_row, move_col = move
            score = -self.negamax_search(move_row, move_col, depth - 1, -beta, -alpha)
            
            if score > best_score:
                best_score = score
                alpha = max(alpha, best_score)
                
                if alpha >= beta:
                    break
        
        self.undo_move(row, col, depth % 2)
        return best_score
    
    def get_candidate_moves(self):
        """获取并排序候选移动"""
        candidates = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if not self.board[i][j].has_piece:
                    candidates.append((i, j))
        
        # 按评分排序，高分优先
        candidates.sort(key=lambda pos: self.board[pos[0]][pos[1]].score, reverse=True)
        return candidates
