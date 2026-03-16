# 第四次作业-推理与规划

## 题目一

定义论域$X$是所有人。

定义谓词：

1. $Student(x)$：表明$x$是学生
2. $Smart(x)$：表明$x$是聪明的
3. $Loves(x, y)$：表明$x$喜欢$y$
4. $Other(x, y)$：表明$x$和$y$不是同一个人
5. $Analysis(x)$：$x$选修
6. $Geometry(x)$：$x$选修

形式化句子：

1. $\forall x(Student(x) \Rightarrow Smart(x))$
2. $\exists x Student(x)$
3. $\exists x (Student(x) \land Smart(x))$
4. $\forall x(Student(x) \Rightarrow \exists y(Student(y) \land Loves(x, y)))$
5.  $\forall x(Student(x) \Rightarrow \exists y(Student(y) \land Other(x, y) \land Loves(x, y)))$
6. $\exists x(Student(x) \land \forall y((Other(x, y) \land Student(y)) \Rightarrow Loves(y ,x)))$
7. $Student(Bill)$
8. $(Analysis(Bill) \land \lnot Geometry(Bill)) \lor (\lnot Analysis(Bill) \land Geometry(Bill))$
9. $Analysis(Bill) \land Geometry(Bill)$
10. $\lnot Analysis(Bill)$
11. $\forall x(Student(x) \Rightarrow \lnot Loves(x, Bill))$

## 题目二

定义论域$X$是所有物体

常量：

1. $A, B, C, D, E, F$：物体常量
2. $Green, Red$：颜色常量

谓词：

1. $On(x, y)$：$x$在$y$上面，其中$x$和$y$都是物体常量
2. $Color(x, y)$：$x$的颜色是$y$，其中$x$是物体常量，$y$是颜色常量
3. $Free(x)$：$x$是空闲的物体，其中$x$是物体常量

4. $Other(x, y)$：$x$和$y$不是同一个物体，其中$x$和$y$都是物体常量

一阶逻辑形式：

1. $On(A, C) \land On(D, E) \land On(D, F)$
2. $Color(A, Green) \land \lnot Color(C, Green)$
3. $\forall x \in X \exists y \in X(Other(x, y) \land On(x, y))$
4. $\forall x \in X(Free(x) \Rightarrow \forall y \in X (Other(x, y) \Rightarrow \lnot On(y, x)))$
5. $\forall x\in X(Color(x, Green) \Rightarrow Free(x))$
6. $\exists x \in X(Color(x, Red) \land \lnot Free(x))$
7. $\forall x \in X((\lnot Color(x, Green) \land On(x, B)) \Rightarrow Color(x, Red))$

## 题目三

### (a)

- **(A)：**对于所有的自然数$x$，都存在一个自然数$y$，使得$x$大于等于$y$。
- **(B)：**对于所有的自然数$y$，都存在一个自然数$x$，使得$x$大于等于$y$。

### (b)

**(A)**为真，当$y = x$的时候，命题成立。

### (c)

**(B)**为真，当$x = y$的时候，命题成立

### (d)

对于
$$
(A) \Rightarrow (B)
$$
可以转化为：
$$
\begin{aligned}
(\forall x \exists y (x \geq y)  \Rightarrow \forall y \exists x(x \geq y)) &\Rightarrow (\forall x \exists y(x \geq y) \Rightarrow \forall x \exists y (y \geq x))\\
&\Rightarrow (\lnot \forall x \exists y (x \geq y)) \lor (\forall x \exists y (y \geq x))\\
&\Rightarrow (\exists x_1 \forall y_1(y_1 > x_1)) \lor (\forall x_2 \exists y_2 (y_2 \geq x_2))
\end{aligned}
$$
对于$\forall x_2 \exists y_2 (y_2 \geq x_2)$，当$y_2 = x_2$时，该命题为真。

因此原命题成立。

### (e)

对于
$$
(B) \Rightarrow (A)
$$
可以转化为：
$$
\begin{aligned}
(\forall y \exists x (x \geq y)) \Rightarrow (\forall x \exists y (x \geq y)) &\Rightarrow \lnot (\forall x \exists y(y \geq x)) \lor (\forall x \exists y (x \geq y))\\
&\Rightarrow (\exists x \forall y (x > y)) \lor (\forall x \exist y (x \geq y))
\end{aligned}
$$
其中对于$\forall x \exists y (x \geq y)$，当$y = x$时，该命题为真。

因此原命题成立。

对于$(d)$和$(e)$两个问题，由于$(A)$和$(B)$都是永真式，因此是显然有逻辑蕴含成立的。

### (f)

证明：$(B) \Rightarrow (A)$，采用反证法有：

- 假设$(B)$为真，因此有$\forall y \exists x (x \geq y)$，目标$(A)$为假，因此有$\lnot \forall x \exists y (x \geq y)$。

- 转化为CNF有：
  $$
  \begin{aligned}
  (\forall y \exists x (x \geq y)) \land (\lnot\forall x \exists y(x \geq y))
  \end{aligned}
  $$

- 进行化简：（定义 $Geq(x, y)$表示$x \geq y$）
  $$
  \begin{aligned}
  (\forall y \exists x Geq(x, y)) \land (\lnot \forall x \exists y Geq(x, y)) &\Rightarrow (\forall x \exists y Geq(y, x)) \land (\exists x \lnot \exists y Geq(x, y))\\
  &\Rightarrow (\forall x \exists y Geq(y, x)) \land (\exists x \forall y\lnot Geq(x, y))\\
  &\Rightarrow \forall x Geq(f(x), x) \land \forall y \lnot Geq(c, y)
  \end{aligned}
  $$

- 观察到此处无法进一步化简，也推不出矛盾。因此反证法至此无法证明或证伪原命题。

但是可以注意到在$(a)$的条件下，$(B)$、$(A)$都是永真式，因此$(B) \Rightarrow (A)$成立。

### (g)

证明：$(A) \Rightarrow (B)$，采用反证法有：

- 假设$(A)$为真，因此$\forall x \exists y (x \geq y)$，目标$(B)$为假，因此有$\lnot \forall y \exists x (x \geq y)$。

- 转化为CNF有：
  $$
  (\forall x \exists y (x \geq y)) \land \lnot(\forall y \exists (x \geq y))
  $$

- 进行化简：（定义 $Geq(x, y)$表示$x \geq y$）
  $$
  \begin{aligned}
  (\forall x \exists y (x \geq y)) \land \lnot(\forall y \exists x (x \geq y)) &\Rightarrow (\forall x \exists y Geq(x, y)) \land (\exists y \lnot \exists xGeq(x, y))\\
  &\Rightarrow (\forall x \exists y Geq(x, y)) \land (\exists y \forall x \lnot Geq(x, y))\\
  &\Rightarrow (\forall x Geq(x, f(x)) \land (\forall y \lnot Geq(c, y))
  \end{aligned}
  $$

- 观察到此处无法进一步化简，也推不出矛盾。因此反证法至此无法证明或证伪原命题。

但是可以注意到在$(a)$的条件下，$(B)$、$(A)$都是永真式，因此$(A) \Rightarrow (B)$成立。

## 题目四

## (1)

谓词：

`IsAmbulance(X)`：$X$是救护车

`IsInInter(X)`：$X$在十字路口中

`IsAt(X, loc)`：$X$在$loc$

`IsPerson(X)`：$X$是人

`Before(X, Y)`：$X$在$Y$的前面

`IsCar(X)`：$X$是汽车

停车规则：

`Stop(X)`: 如果前面有人，则停下；如果前面是救护车则停下；如果前面有车，并且车在十字路口中，则停下。

$[IsPerson(Y) \land Before(Y, X)] \lor [IsAmbulance(Y) \land Before(Y, X)] \lor [IsCar(Y) \land Before(Y, X) \land IsInInter(Y)]$

化简为：
$$
Before(Y, X) \land[IsPerson(Y) \lor IsAmbulance(Y) \lor IsCar(Y) \land IsInInter(Y)]
$$

## (2)

### 一号小车

由于小车$X$前面没有东西，因此$Before(Y, X)$的知识库中找不到存在的$Y$，因此上述定义的$Stop(X)$的值为$false$，不需要停车。

### 二号小车

小车$X$前面有蓝车$Y$，其中$Before(Y)$、$IsCar(Y)$、$IsInInter(Y)$的值为$true$，因此上述定义的$Stop(X)$的值为$true$，需要停车。

### 三号小车

小车$X$前面没有东西，但是侧前方有人。这需要考虑$before(Y, X)$中所定义的范围，这里假设人$Y$不在小车$X$的$before$范围中，因此上述定义的$Stop(X)$的值为$false$，不需要停车。

## (3)

### 动作空间

`forward`、`backward`、`turnRight`、`turnLeft`

向前一格、向后一格、向右转90°、向左转90°.

### 状态空间

`loc(x, y)`、`direction`

当前位置、当前方向

定义：`dir = [[0, 1],[1, 0],[0, -1], [-1, 0]]`，通过`dir[direction]`获取当前位置

### 状态转移

`forward()`：`loc(x, y) += dir[direction]`.

`backward()`：`loc(x, y) -= dir[direction]`.

`turnRight()`：`direction = (direction + 1) % 4`.

`turnLeft()`：`direction = (direction + 4 - 1) % 4`.

### 奖励函数

可能需要一些来自环境的参数，比如：

`inRoad(X)`：判断$X$是否还在道路上（如果保持在道路上开能加分，反之扣分）

`crashCar(X, Y)`：汽车$X$和汽车$Y$相撞（扣分）

`crashPerson(X, Y)`：汽车$X$和行人$Y$相撞（相比撞车应该扣更多分）

`reached(X)`：判断$X$是否到达终点或者完成目标（达成目标加分）

`getCloseEnd(X)`：判断$X$是否更靠近终点（如果远离终点则扣分，靠近不加分）

那么基于以上五个函数可以设计以下的奖励函数：
$$
Reward = inRoad(X) + crashCar(X, Y) + crashPerson(X, Y) + reached(X) + getCloseEnd(X)
$$
加分和扣分的具体实现主要依赖于相关函数的返回值。

## (4)

在状态空间中引入：`speed`，动作空间引入：`fast`、`slow`，并给出相关的状态转移。

此外之前的`forward`和`backward`两个动作在进行位移的时候，位移量需要乘上`speed`。

然后环境中可以对部分路径进行限速，并且给出一些类似判断是否超速的函数：

`overSpeed(X, loc)`：汽车$X$在$loc$出超出了这个路段的限速

并将其引入到奖励函数中。

此外还能对一些动作空间执行给出前置要求，例如只有在`speed <= 30`时，才可以执行`turnRight`和`turnLeft`操作。

## (5)

### 1. 输入以及知识库搭建

将初始状态的图片作为输入传入，利用视觉模型对图片中的信息进行分析提取，并更新知识库中。比如更新`IsAt(X)`,`IsInInter(X)`等这类谓词。

### 2. 行动

根据更新后的知识库，并利用各种实现规定好的规则，使每一个Agent进行一次状态转移。

并更新行动一次后的知识库。

### 3. 对结果进行分析

对新知识库进行分析，计算奖励函数，将其的奖励进行输出，供Agent学习。

