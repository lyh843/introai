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
        return np.all(board != 0)