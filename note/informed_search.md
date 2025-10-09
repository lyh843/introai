# 有信息搜索

又名“启发式搜索”

启发式信息：

- 估计离目标状态有多远的信息
- 不同的问题需要设计不同的启发信息
- 例如：曼哈顿距离、欧式距离

## 一、 贪婪搜索(greedy search)

### 1. 贪婪算法(greedy algorithm)

又称贪心算法，指在每一步选择中都采取在当前状态下最好或最优（即最有利）的选择，从而希望导致结果是最好或最优的算法。

没有从总体上考虑其他可能情况，每次选取局部最优解，一般不能得到最优解。

#### 2. 概念

- 策略：每一步均扩展距离目标状态更近的节点。

  启发式信息：估计当前状态距离目标状态的距离

- Common case： 距离目标越来越近

- Bad case: 非完备、非最优、依赖启发式函数

## 二、 A\*搜索

### 1. 概念：

$$
f(n) = g(n) + h(n)
$$

$g(n)$表示从起始节点到节点$n$的开销代价值，$h(n)$表示从节点$n$到目标节点路径中所估算的最小开销代价值。

**评价函数**$f(n)$可视为经过节点$n$、具有最小开销代价值的路径。

### 2\*. A\*算法的完备性

在一些常见的搜索问题中，状态数量是有限的，此时图搜索A\*算法和排除环路的树搜索A\*算法均是完备的。

在更普遍的情况下，如果所求问题和启发式函数满足以下条件，则A\*算法是完备的：

1. 搜索树中分支数量是有限的，即每个节点的后继节点数量是有限的。
2. 单步代价的下界是一个正数
3. 启发函数有下界

### 3\*. A\*算法的最优性

如何修改启发式信息可以使算法找到最优解？

1. 可采纳性(admissible)：对于任意节点$n$，有$h(n) \leq h^*(n)$

   启发式函数不会过高估计从节点$n$到终止节点所应该付出的代价。（估计代价小于等于实际代价）

2. 一致性：对于每个节点$n$和通过任一行动$a$生成的$n$的每个后继节点$n'$，有$h(n) \leq cost(n, a, n') + h(n')$

### 4. 代码

```python
def A_star(heuristic):
    Frontier = priority_queue()
    Frontier.push((start_state, []), 0 + heuristic(start_state))
    
    visited = {}
    
    while Frontier.isEmpty() == 0:
        state, actions = Frontier.pop()
        if state in visited and get_cost_of_actions(state) + heurisitc(state) >= visited[state]:
            continue
        visited[state] = get_cost_of_actions(state) + heurisitc(state)
        if is_target_state(state):
            return actions
        for next_state, next_direction in get_successors(state):
            Frontier.push((next_state, actions + [next_direction]), get_cost_of_actions(actions + [next_direction] +heuristic(next_state)))
     return None
```



## 三、 启发式函数（heuristic function）

启发式搜索的关键在于如何设计启发式函数。

可采纳的启发式函数可以看做松弛问题(relaxed problems)的解。

### 例子：八数码问题

1. 不在正确位置的棋子数。
2. 所有棋子到目标位置的距离和（曼哈顿距离）

如果启发式函数$h(n) = 0$ $\Rightarrow$ 等价于一致性代价搜索

如果采用真实的代价作为启发式函数 $\Rightarrow$ 最佳情况，但是不可能实现