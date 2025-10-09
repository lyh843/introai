# 无信息搜索

## 一、搜索问题

### 1. 概念

可以用6个组分部分形式描述：

​	状态空间、初始状态、动作、状态转移、目标测试、路径/代价

问题的解是从初始状态到目标状态的一组行动序列，所有解里面代价最小的解即为最优解。

### 2. 搜索问题求解

- 扩展当前的状态，在当前状态下采用各种行动，生成新的状态
- 所有待扩展的节点称为**边缘节点**
- 不断从边缘节点中选择节点并扩展，直到到达目标状态，或者没有状态可以扩展

### 3. 搜索策略

搜索策略的主要区别在于如何选择要扩展的状态。

评估搜索算法性能的指标：

- 完备性：能否保证找到解
- 最优性：能否找到最优解
- 时间复杂度：找到解需要花费多长时间
- 空间复杂度：在执行搜索的过程总需要多少存储空间

## 二、无信息搜索

除了问题定义中给定的状态信息外，没有任何附加信息。

### 1. 宽度优先搜索(breadth-first search, BFS)

#### 1. 概念

先拓展根节点，接着拓展根节点的所有后继节点，然后再拓展它们的后继，以此类推。

一般地，在下一层的任何节点拓展之前，搜索树本层深度的所有节点应该都已经扩展过。

#### 2. 性能分析

- 时间复杂度：$1 + b + b^2 + b^3 + \cdots +b^d = O(b^d)$
- 空间复杂度：$O(b^d)$
- 完备性：yes
- 最优性：yes（如果所有行动代价相同）

#### 3. 代码实现

```python
def breadth_first_search():
    Frontier = deque()	# 存储边缘节点，采用队列这一数据结构，先进先出
    Frontier.pushback((startstate, []))		# 插入（初始节点，当前的动作序列）
    
    visited = set()	# 记录已访问的状态，避免重复访问（图搜索）
    visited.append(startstate)
    
    while Frontier.isEmpty == 0:	# 只要还有边缘节点，就继续搜索。
        state, actions = Frontier.popfront()		# pop出一个这次拓展的节点
        
        if is_target_state(state):
            return actions	# 如果当前状态是目标状态，返回动作序列
        
        for next_state, next_direciton in get_successors(state):
            # 遍历所有当前节点的子节点，插入边缘节点的队列尾部
            if next_state not in visited:
                visited.append(next_state)
            	Frontier.pushback((next_state, actions + [next_direciton]))
```

### 2. 深度优先搜索(depth-first search, DFS)

#### 1.概念

总是拓展当前边缘节点中最深的节点。

#### 2. 性能分析

- 时间复杂度$

- 空间复杂度：$O(bm)$

  只需要存储一条从根节点到叶节点的路径，以及该路径上每个节点的所有未被拓展的兄弟节点

- 完备性：No

- 最优性：No

#### 3. 代码实现

```python
def depth_first_search():
    Frontier = stack()	# 存储边缘节点，采用栈这一数据结构，不断访问子节点
    Frontier.push((startstate,[]))	# 插入（初始节点，当前的动作序列）
    
    visited = set()	# 记录已访问的状态，避免重复访问（图搜索）
    
    while Frontier.isEmpty() == 0:	# 只要还有边缘节点，就继续搜索。
        state, actions = Frontier.pop()	# pop出一个这次拓展的节点
        
        if state not in visited:
            visited.append(state)
            if is_target_state(state):	# 如果当前状态是目标状态，返回动作序列
                return actions
            
            for next_state, next_direciton in get_successors(state):
                Frontier.push((next_state, actions + [next_direciton]))
```

### 3. 迭代加深的深度优先搜索(iterative deepening search)

#### 1. 概念

每次深度搜索时，给予一个允许搜索的最深深度。通过不断增大最深深度，从而进行搜索。

#### 2. 性能分析

- 时间复杂度：$O(b^d)$
- 空间复杂度：$O(bd)$
- 完备性：yes
- 最优性：yes（如果所有动作代价相同）

#### 3. 代码实现

```python
def iterative_deepening_search():
    def deepening_search(limit):
        Frontier = stack()	# 存储边缘节点，采用栈这一数据结构，不断访问子节点
        Frontier.push((start_state,[], 0))	# 插入（（初始节点， 当前深度），当前的动作序列）
		
        visited = set()	# 记录已访问的状态，避免重复访问（图搜索）

        while Frontier.isEmpty() == 0:	# 只要还有边缘节点，就继续搜索。
            state, actions, level = Frontier.pop()	# pop出一个这次拓展的节点
			if level > limit:
                continue
            if state not in visited:
                visited.append(state)
                if is_target_state(state):	# 如果当前状态是目标状态，返回动作序列
                    return actions

                for next_state, next_direction in get_successors(state):
                    Frontier.push((next_state, actions + [next_direction], level + 1))
         return None
    limit = 0
    result = None
    while result is None:
        limit += 1
        result = deepening_search(limit)
   	return result
        
```



### 4. 一致性代价搜索(uniform_cost_search)

#### 1. 概念

拓展路径消耗最小的节点

#### 2. 性能分析

- 时间复杂度：$O(b^{\frac{c^*}{\epsilon}})$
- 空间复杂度：$O(b^{\frac{c^*}{\epsilon}})$
- 完备性：yes， 如果每一步的代价$\geq \epsilon (\epsilon > 0)$
- 最优性：yes

#### 3. 代码

```python 
def uniform_cost_search():
    Frontier = priority_queue()
    Frontier.push((start_state, []), 0)
    
    visited = {}
    
    while Frontier.isEmpty() == 0:
        state, actions = Frontier.pop()
        
        if state in visited and visited[state] <= get_cost_of_actions(actions):
            continue
            
        visited[state] = get_cost_of_actions(actions)
           
        if is_target_state(state):
   	        return actions
        
        for next_state, next_direction in get_successors(state):     		
            Frontier.push((next_state, actions + [next_direction]), get_cost_of_actions(actions + [next_direction]))
     return None
        
```