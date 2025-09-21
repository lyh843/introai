import numpy as np

# 超参数
LEVEL = 3       # 极大极小搜索深度
DIST = 2        # 搜索扩展区域
NUM = 15        # 每层筛选前 NUM 个候选点
W = 1           # 防守/进攻比重

scores = {
    "Five": 100000,
    "LIVE_FOUR": 100000,
    "DEATH_FOUR": 50000,
    "LIVE_THREE": 5000,
    "SLEEP_THREE": 1000,
    "LIVE_TWO": 100,
}

class Search:
    def __init__(self, player, board_size=15):
        self.player = player
        self.opponent = 3 - player
        self.board_size = board_size

    def make_move(self, board):
        """兼容 play_game 的调用方式，只接收 board"""
        # 空棋盘直接下中点
        if (board == 0).all():
            return (len(board) // 2, len(board) // 2)

        area = self.search_area(board)
        up, down, left, right = area
        value = float("-inf")
        result_loc = (0, 0)
        record = []

        # 筛选候选点
        for i in range(up, down + 1):
            for j in range(left, right + 1):
                if board[i][j] != 0:
                    continue
                temp_score = self.judge_count(board, (i, j), self.player)
                record.append((temp_score, (i, j)))

        record.sort(reverse=True, key=lambda x: x[0])
        record = record[:NUM]

        # 极大极小搜索
        for _, (i, j) in record:
            board[i][j] = self.player
            temp = self.maxmin(board, False, self.update_area(board, area, (i, j)), 1)
            board[i][j] = 0
            if temp > value:
                value = temp
                result_loc = (i, j)

        return result_loc

    def evaluate(self, board, area, is_player):
        value = 0
        for i in range(area[0], area[1] + 1):
            for j in range(area[2], area[3] + 1):
                if board[i][j] == self.player:
                    player_score = self.judge_count(board, (i, j), self.player)
                    if is_player and player_score >= scores["DEATH_FOUR"]:
                        return 999999
                    value += player_score
                elif board[i][j] == self.opponent:
                    opponent_score = self.judge_count(board, (i, j), self.opponent)
                    if (not is_player) and opponent_score >= scores["DEATH_FOUR"]:
                        return -999999
                    value -= W * opponent_score
        return value

    def maxmin(self, board, to_max, area, level, alpha=float("-inf"), beta=float("inf")):
        if level == LEVEL:
            return self.evaluate(board, area, to_max)

        up, down, left, right = area
        record = []
        if to_max:
            value = float("-inf")
            for i in range(up, down + 1):
                for j in range(left, right + 1):
                    if board[i][j] != 0:
                        continue
                    score = self.judge_count(board, (i, j), self.player)
                    record.append((score, (i, j)))
            record.sort(reverse=True, key=lambda x: x[0])
            record = record[:NUM]
            for _, (i, j) in record:
                board[i][j] = self.player
                temp = self.maxmin(board, False, self.update_area(board, area, (i, j)), level + 1, alpha, beta)
                board[i][j] = 0
                value = max(value, temp)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        else:
            value = float("inf")
            for i in range(up, down + 1):
                for j in range(left, right + 1):
                    if board[i][j] != 0:
                        continue
                    score = self.judge_count(board, (i, j), self.opponent)
                    record.append((score, (i, j)))
            record.sort(reverse=True, key=lambda x: x[0])
            record = record[:NUM]
            for _, (i, j) in record:
                board[i][j] = self.opponent
                temp = self.maxmin(board, True, self.update_area(board, area, (i, j)), level + 1, alpha, beta)
                board[i][j] = 0
                value = min(value, temp)
                beta = min(beta, value)
                if beta <= alpha:
                    break
        return value

    def search_area(self, board):
        board_size = len(board)
        area = [board_size - 1, 0, board_size - 1, 0]  # up, down, left, right
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] != 0:
                    area[0] = min(area[0], max(0, i - DIST))
                    area[1] = max(area[1], min(board_size - 1, i + DIST))
                    area[2] = min(area[2], max(0, j - DIST))
                    area[3] = max(area[3], min(board_size - 1, j + DIST))
        if area[1] < area[0] or area[3] < area[2]:
            return [0, board_size - 1, 0, board_size - 1]
        return area

    def update_area(self, board, area, loc):
        new_area = area.copy()
        if loc[0] - DIST < new_area[0]:
            new_area[0] = max(loc[0] - DIST, 0)
        if loc[0] + DIST > new_area[1]:
            new_area[1] = min(loc[0] + DIST, len(board) - 1)
        if loc[1] - DIST < new_area[2]:
            new_area[2] = max(loc[1] - DIST, 0)
        if loc[1] + DIST > new_area[3]:
            new_area[3] = min(loc[1] + DIST, len(board) - 1)
        return new_area

    def judge_count(self, board, loc, target):
        x, y = loc
        board_size = len(board)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        max_score = 0
        for dx, dy in directions:
            count = 1
            blocked_front = blocked_back = False
            # 正向
            for i in range(1, 5):
                nx, ny = x + dx * i, y + dy * i
                if not (0 <= nx < board_size and 0 <= ny < board_size):
                    blocked_front = True
                    break
                if board[nx][ny] == target:
                    count += 1
                elif board[nx][ny] != 0:
                    blocked_front = True
                    break
                else:
                    break
            # 反向
            for i in range(1, 5):
                nx, ny = x - dx * i, y - dy * i
                if not (0 <= nx < board_size and 0 <= ny < board_size):
                    blocked_back = True
                    break
                if board[nx][ny] == target:
                    count += 1
                elif board[nx][ny] != 0:
                    blocked_back = True
                    break
                else:
                    break
            if count >= 5:
                return scores["Five"]
            elif count == 4 and not blocked_front and not blocked_back:
                return scores["LIVE_FOUR"]
            elif count == 4:
                return scores["DEATH_FOUR"]
            elif count == 3 and not blocked_front and not blocked_back:
                max_score = max(max_score, scores["LIVE_THREE"])
            elif count == 3:
                max_score = max(max_score, scores["SLEEP_THREE"])
            elif count == 2 and not blocked_front and not blocked_back:
                max_score = max(max_score, scores["LIVE_TWO"])
        return max_score
