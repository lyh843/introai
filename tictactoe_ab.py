# tictactoe_ab.py
# 3x3 井字棋。X 为人类，O 为电脑（AI）。
# 代码包含两个搜索版本：
#  - minimax_simple: 经典无剪枝的 minimax（可运行）。
#  - minimax_alpha_beta: 带 α-β 参数的版本，关键处用 TODO 留空，供你实现剪枝逻辑。
#
# 目标：你实现 α-β 的更新与剪枝，然后将 get_best_move 中的 use_alpha_beta 设为 True 验证加速与等价性。

from typing import List, Optional, Tuple
import math

PLAYER_HUMAN = 'X'
PLAYER_AI = 'O'
EMPTY = ' '

WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),  # rows
    (0,3,6), (1,4,7), (2,5,8),  # cols
    (0,4,8), (2,4,6)            # diags
]

class TicTacToe:
    def __init__(self):
        # 用一维长度9的列表表示棋盘，索引从0到8
        self.board: List[str] = [EMPTY] * 9

    # ---- 基本工具函数 ----
    def print_board(self):
        b = self.board
        lines = []
        for r in range(3):
            row = [b[3*r + c] if b[3*r + c] != EMPTY else str(3*r + c + 1) for c in range(3)]
            lines.append(' | '.join(row))
        print('\n---------\n'.join(lines))

    def available_moves(self) -> List[int]:
        return [i for i, v in enumerate(self.board) if v == EMPTY]

    def make_move(self, idx: int, player: str):
        self.board[idx] = player

    def undo_move(self, idx: int):
        self.board[idx] = EMPTY

    def is_winner(self, player: str) -> bool:
        b = self.board
        return any(b[a]==player and b[b_idx]==player and b[c]==player for (a,b_idx,c) in WIN_LINES)

    def is_draw(self) -> bool:
        return all(cell != EMPTY for cell in self.board) and not (self.is_winner(PLAYER_HUMAN) or self.is_winner(PLAYER_AI))

    def game_result(self) -> Optional[str]:
        # 返回获胜者 'X' 或 'O'，平局返回 'draw'，未结束返回 None
        if self.is_winner(PLAYER_HUMAN):
            return PLAYER_HUMAN
        if self.is_winner(PLAYER_AI):
            return PLAYER_AI
        if all(cell != EMPTY for cell in self.board):
            return 'draw'
        return None

    # ---- 评价函数 ----
    def evaluate(self, depth: int) -> int:
        """
        评估终局：
        - 若 AI 获胜，返回 +10 - depth（尽快获胜得分更高）
        - 若 人类 获胜，返回 -10 + depth（尽快让人类输得更差）
        - 平局返回 0
        depth 用来偏好更快的胜利或更晚的失败
        """
        winner = self.game_result()
        if winner == PLAYER_AI:
            return 10 - depth
        if winner == PLAYER_HUMAN:
            return depth - 10
        return 0

    # ---- 经典 minimax（无剪枝） ----
    def minimax_simple(self, depth: int, maximizing: bool) -> int:
        """
        经典递归 minimax。
        当达到终局时返回评价值；否则枚举所有可行动作并递归。
        该函数可运行，用于对比与验证 α-β 实现的正确性。
        """
        result = self.game_result()
        if result is not None:
            return self.evaluate(depth)

        if maximizing:
            best = -math.inf
            for mv in self.available_moves():
                self.make_move(mv, PLAYER_AI)
                val = self.minimax_simple(depth + 1, False)
                self.undo_move(mv)
                if val > best:
                    best = val
            return best
        else:
            best = math.inf
            for mv in self.available_moves():
                self.make_move(mv, PLAYER_HUMAN)
                val = self.minimax_simple(depth + 1, True)
                self.undo_move(mv)
                if val < best:
                    best = val
            return best

    # ---- minimax 带 α-β 参数（挖空位置示例） ----
    def minimax_alpha_beta(self, depth: int, alpha: float, beta: float, maximizing: bool) -> int:
        """
        带 α-β 剪枝的 minimax。
        关键插入点用 TODO 标注。你需要在这些位置写上：
          - 在更新 value 后，更新 alpha 或 beta：
                alpha = max(alpha, value)  （当 maximizing）
                beta  = min(beta, value)  （当 minimizing）
          - 检查是否满足剪枝条件并跳出循环：
                if alpha >= beta: break  （常见形式）
        函数签名中传入初始 alpha=-inf, beta=+inf。
        当前实现不做剪枝（保留参数以便你填充），但逻辑与无剪枝版本等价。
        实现后，将 get_best_move 中 use_alpha_beta=True 以启用。
        """
        result = self.game_result()
        if result is not None:
            return self.evaluate(depth)

        if maximizing:
            value = -math.inf
            for mv in self.available_moves():
                self.make_move(mv, PLAYER_AI)
                val = self.minimax_alpha_beta(depth+1, alpha, beta, False)
                self.undo_move(mv)
                if val > value:
                    value = val

                # 正确更新
                alpha = max(alpha, value)

                # 剪枝
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for mv in self.available_moves():
                self.make_move(mv, PLAYER_HUMAN)
                val = self.minimax_alpha_beta(depth+1, alpha, beta, True)
                self.undo_move(mv)
                if val < value:
                    value = val

                # 正确更新
                beta = min(beta, value)

                # 剪枝
                if alpha >= beta:
                    break
        return value

    # ---- 选择最佳落子 ----
    def get_best_move(self, use_alpha_beta: bool=False) -> int:
        """
        返回最佳落子索引（0-8）。
        若 use_alpha_beta=True，则调用 minimax_alpha_beta（目前仍需你补全剪枝逻辑）。
        否则使用可运行的 minimax_simple。
        """
        best_move = -1
        if use_alpha_beta:
            best_value = -math.inf
            alpha = -math.inf
            beta = math.inf
            for mv in self.available_moves():
                self.make_move(mv, PLAYER_AI)
                val = self.minimax_alpha_beta(1, alpha, beta, False)
                self.undo_move(mv)
                if val > best_value:
                    best_value = val
                    best_move = mv
            return best_move
        else:
            best_value = -math.inf
            for mv in self.available_moves():
                self.make_move(mv, PLAYER_AI)
                val = self.minimax_simple(1, False)
                self.undo_move(mv)
                if val > best_value:
                    best_value = val
                    best_move = mv
            return best_move

# ---- 交互式对局（人类 vs AI） ----
def play():
    g = TicTacToe()
    current = PLAYER_HUMAN  # 人先手
    print("井字棋 1-9，1左上，9右下。输入 q 退出。")
    while True:
        g.print_board()
        res = g.game_result()
        if res is not None:
            if res == 'draw':
                print("平局。")
            else:
                print(f"赢家：{res}")
            break

        if current == PLAYER_HUMAN:
            s = input("你的落子（1-9）：").strip()
            if s.lower() == 'q':
                print("退出。")
                break
            if not s.isdigit():
                print("输入无效。请输入 1-9。")
                continue
            idx = int(s) - 1
            if idx < 0 or idx > 8 or g.board[idx] != EMPTY:
                print("该格不可落子，请重试。")
                continue
            g.make_move(idx, PLAYER_HUMAN)
            current = PLAYER_AI
        else:
            # 切换 use_alpha_beta=True 在你实现剪枝后以测试加速效果
            ai_move = g.get_best_move(use_alpha_beta=True)
            print(f"AI 下在 {ai_move + 1}")
            g.make_move(ai_move, PLAYER_AI)
            current = PLAYER_HUMAN

if __name__ == '__main__':
    play()
