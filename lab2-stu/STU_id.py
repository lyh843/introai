from agent import Agent

class myAgent(Agent):
    def __init__(self, player):
        super().__init__(player)
    
    def make_move(self, board):
        
        return super().make_move(board)
    
    def score(self, board):
        """
        分数评估函数，对传入棋盘的分数进行评价

        Args:
            board (_type_): _description_
        """
        