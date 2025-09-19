import numpy as np
import agent


# 超参数
# 每次拓展节点的深度
LEVEL = 2
# 下棋时考虑的距离有棋区域的范围
DIST = 2

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
        new_board = board
        area = self.search_area(board)
        x, y = self.maxmin(board, True, area, 0)
        up = area[0], down = area[1], left = area[2], right = area[3]
        value = float('-inf')
        result_loc = (0, 0)
        for i in range(up, down + 1, 1):
            for j in range(left, right + 1):
                if board[i][j] != 0 : continue
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
        
    
    def maxmin(self, board, to_max, area, level = 0):
        """
        进行极大极小值判断以及剪枝处理。
        返回当前节点的value
        Args:
            board (_type_): _description_
            to_max (bool): 目前是否为极大值模型
        """
        if level == LEVEL:
            return self.evaluate(board)
        up = area[0], down = area[1], left = area[2], right = area[3]
        new_board = board
        value = 0
        if to_max:
            value = float('-inf')
            for i in range(up, down + 1, 1):
                for j in range(left, right + 1, 1):
                    if board[i][j] != 0 : continue
                    new_board[i][j] = self.player
                    temp = self.maxmin(new_board, False, self.update_area(board, area, (i, j)), level + 1)
                    if temp > value:
                        value = temp
        else:
            value = float('inf')
            for i in range(up, down + 1, 1):
                for j in range(left, right + 1, 1):
                    if board[i][j] != 0: continue
                    new_board[i][j] = self.opponent
                    temp = self.maxmin(new_board, True, self.update_area(board, area, (i, j)), level + 1)
                    if temp < value:
                        value = temp
                        
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
        if loc[0] - DIST < area[0]:
            area[0] = max(loc[0] - DIST, 0)
        if loc[0] + DIST > area[1]:
            area[1] = min(loc[0] + DIST, len(board) - 1)
        if loc[1] - DIST < area[2]:
            area[2] = max(loc[1] - DIST, 0)
        if loc[1] + DIST > area[3]:
            area[3] = min(loc[1] + DIST, len(board) - 1)
        
        return area