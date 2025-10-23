# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
MAX_DEPTH=1000

"""
在search.py​​中，您将实现通用搜索算法
PACMAN代理商（在searchagents.py中）。
"""

import util
import heapq

class SearchProblem:
    """
本课程概述了搜索问题的结构，但没有实现
任何方法（在面向对象的术语中：抽象类）。

您永远不需要更改此类的任何内容。
    """

    def getStartState(self):
        """
        返回搜索问题的开始状态。
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
         状态：搜索状态

且仅当状态是有效的目标状态时返回true。
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          状态：搜索状态

对于给定状态，这应该返回三倍的列表（继任者，
行动，步长），其中“继任者”是当前的继任者
状态“行动​​”是到达那里所需的动作，而“ stepcost”是
扩展到该继任者的增量成本。
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
返回一系列解决tinymaze的动作。对于任何其他迷宫，
移动序列将是不正确的，因此仅将其用于Tinymaze。
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
首先搜索搜索树中最深的节点。

您的搜索算法需要返回到达该操作的列表
目标。确保实现图形搜索算法。

首先，您可能需要尝试一些这些简单命令
了解正在传递的搜索问题：

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    Frontier = util.Stack()
    Visited = []
    Frontier.push((problem.getStartState(), []))
    
    while Frontier.isEmpty() == 0:
        state, actions = Frontier.pop()
        if problem.isGoalState(state):
            return actions
        for next in problem.getSuccessors(state):
            n_state = next[0]
            n_direction = next[1]
            if n_state not in Visited:
                Frontier.push((n_state, actions + [n_direction]))
                Visited.append(state)

    util.raiseNotDefined()
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    
#! 例题答案如
#     "*** YOUR CODE HERE ***"
    Frontier = util.Queue()
    Visited = []
    Frontier.push( (problem.getStartState(), []) )
    Visited.append( problem.getStartState() )

    while Frontier.isEmpty() == 0:
        state, actions = Frontier.pop()
        if problem.isGoalState(state):
            return actions 
        for next in problem.getSuccessors(state):
            n_state = next[0]
            n_direction = next[1]
            if n_state not in Visited:
                Frontier.push( (n_state, actions + [n_direction]) )
                Visited.append( n_state )

def iterativeDeepeningSearch(problem):
    """
    Search using iterative deepening search.
    
    Iterative deepening search combines the space efficiency of depth-first search
    with the optimality of breadth-first search. It performs a series of depth-limited
    searches with increasing depth limits until a solution is found.
    
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """   
    def depthLimitedSearch(problem, limit):
        """
        Helper function to perform depth-limited search with a given depth limit.
        Returns the solution path if found within the limit, None otherwise.
        """
        "*** YOUR CODE HERE ***"
        Frontier = util.Stack()
        Visited = []
        level = 0
        Frontier.push((problem.getStartState(), [], level))
        Visited.append(problem.getStartState())
        while Frontier.isEmpty() == 0:
            state, actions, curr_level = Frontier.pop()
            if problem.isGoalState(state):
                return actions
            for next in problem.getSuccessors(state):
                n_state = next[0]
                n_direction = next[1]
                if n_state not in Visited and curr_level < limit:
                    Frontier.push((n_state, actions + [n_direction], curr_level + 1))
                    Visited.append(n_state)
        

    depth_limit = 0
    while True:
        result = depthLimitedSearch(problem, depth_limit)
        if result is not None:
            return result
        depth_limit += 1
        if depth_limit > MAX_DEPTH:  # maximum
            break
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    Frontier = util.PriorityQueue()
    Visited = []
    Frontier.push((problem.getStartState(), []), 0)
    Visited.append(problem.getStartState())
    while Frontier.isEmpty() == 0:
        state, actions = Frontier.pop()
        if problem.isGoalState(state):
            return actions
        for next in problem.getSuccessors(state):
            n_state = next[0]
            n_direction = next[1]
            if n_state not in Visited:
                Frontier.push((n_state, actions + [n_direction]), problem.getCostOfActions(actions + [n_direction]))
                Visited.append(n_state)
            
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    Frontier = util.PriorityQueue()
    Visited = []
    Frontier.push((problem.getStartState(), []), 0 + heuristic(problem.getStartState(), problem))
    Visited.append(problem.getStartState())
    
    while Frontier.isEmpty() == 0:
        state, actions = Frontier.pop()
        if state in Visited:
            continue
        Visited.append(state)
        if problem.isGoalState(state):
            return actions
        for next in problem.getSuccessors(state):
            n_state = next[0]
            n_direction = next[1]
            Frontier.push((n_state, actions + [n_direction]), problem.getCostOfActions(actions + [n_direction]) + heuristic(n_state, problem))

    
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
iter = iterativeDeepeningSearch
