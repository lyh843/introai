# 推理与规划

## 零、引入

### 1. 感知到认知

**人工智能的发展：**

$Comuptation \rightarrow Perception \rightarrow Cognition \rightarrow Action$ 

计算$\rightarrow$感知$\rightarrow$认知$\rightarrow$行动

### 2. 推理（Reasoning）

推理是进行思维模拟的基本形式，是从一个或几个已知的判断（前提）推出新判断（结论）的过程。

**分类：**演绎推理、归纳推理、反绎推理、因果推理

#### 演绎推理（Deductive Reasoning）

从**一般性前提**出发，通过演绎推导，得到结论的过程。

例子：数学推理、形式逻辑推理。

#### 归纳推理（Inductive Reasoning）

从**个别事实**出发，推导出一般性知识作为结论。

#### 反绎推理（Abductive Reasoning）

最佳解释推理，观察到某个现象，推出最可能得原因

例子：医疗诊断类任务

#### 因果推理（Causal Reasoning）

推理事件与事件之间的因果关系

相关性与因果性：鸡叫，天就会亮

**Judea Pearl** 的因果三层级：

- **关联**：如果$X$发生，$Y$通常是什么？
- **干预**：如果我做了$X$，$Y$会怎么样？
- **反事实**：如果我没做$X$，会发生什么？

### 3. 符号主义人工智能

智能可以通过符号+规则来表达和推理

### 4. 逻辑智能体(Logic / knowledge based Agent)

**知识库（Knowlegde Base, KB）：**一系列语句的集合，语句用某种形式来表达**（符号）**

**感知（Perception）：**感知环境状态并转化为符号化信息，写入知识库**（符号接地，Symbolic Grounding）**

**推理（Reasoning）：**知识库进行推理，新知识加入知识库，得出下一步行动

---

## 一、逻辑（Logic）

### (1) 基础概念

**语法（syntax）：**规定所有合规的语句

**语义（semantics）：**定义了所有语句的含义，或者说在每个可能世界的真值

**蕴含/蕴涵（Entailment）：**一个语句在逻辑上引发另一语句，$\alpha \vdash \beta$

知识库 $KB \vdash \beta$ 当且仅当 $\beta$ is true in all worlds where $KB$ is true. 

### (2) 命题逻辑（Propositional Logic）

 应用一套**形式化规则**对以**符号表示的描述性陈述**进行推理的系统。

**命题（或逻辑表达式）：**一个能够确定真假的陈述句

#### 1. 逻辑连接词

| 逻辑连接词 | 表示形式             |
| ---------- | -------------------- |
| 与(and)    | $p\land q$           |
| 或(or)     | $p\lor q$            |
| 非(not)    | $\lnot p$            |
| 蕴含式     | $p\rightarrow q$     |
| 当且仅当   | $p\leftrightarrow q$ |

#### 2. 归结

在两个表达式之间进行，把冲突的部分优化掉，消去互补文字。$\alpha \lor \beta , \lnot \beta \rightarrow \alpha$

#### 3. 合取范式（CNF）

#### 4. 归纳算法

证明，$KB \rightarrow \alpha$，采用反证法

- 假设$KB$为真，目标$\alpha$为假，即$(KB \land \lnot \alpha)$是不可满足的
- 将$(KB\land \lnot \alpha)$转换为CNF
- 不断应用归结规则，产生新的字句
- 直到推导出矛盾

#### 5. 扩展：SAT与SMT

- 布尔可满足性问题（SAT）：给定一个布尔公式，判断是否存在一个变量赋值，使公式为真
- SMT(Satisfiability Modulo Theories)：在SAT的基础上加入数学相关的（如算术、数组、位向量、几何等）可满足性问题

#### 6. 霍恩子句与确定子句

- **确定子句（definite clause）**：文字的析取式，其中只有一个为正文字。（如：$\lnot B_{11} \land \lnot P_{12} \lor P_{21}$）
- **霍恩子句（horn caluse）**：文字的析取式，最多只有一个为正文字
- 每个确定子句都可以写成一个蕴涵式

#### 7. 前向推理

#### 8. 后向推理

#### 9. 命题逻辑的局限性

在命题逻辑中，每个陈述句是最基本的单位(即原子命题)，无法对原子命题进行分解，因此在命题逻辑中，**不能表达局部与整体、一般与个别的关系**

