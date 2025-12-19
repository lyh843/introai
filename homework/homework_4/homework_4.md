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

### (f)

证明：$(B) \Rightarrow (A)$，采用反证法有：

- 假设$(B)$为真，因此有$\forall y \exists x (x \geq y)$，目标$(A)$为假，因此有$\lnot \forall x \exists y (x \geq y)$。

- 转化为CNF有：
  $$
  \begin{aligned}
  (\forall y \exists x (x \geq y)) \land (\lnot\forall x \exists y(x \geq y))
  \end{aligned}
  $$

- 进行化简：
  $$
  \begin{aligned}
  (\forall y \exists x (x \geq y)) \land (\lnot \forall x \exists y(x \geq y)) &\Rightarrow (\forall x \exists y (y \geq x)) \land (\exists x \lnot \exists y (x \geq y))\\
  &\Rightarrow (\forall x \exists y (y \geq x)) \land (\exists x \forall y\lnot(x \geq y))\\
  &\Rightarrow (\forall x \exists y (y \geq x)) \land (\exists x \forall y (y > x))
  \end{aligned}
  $$

- 观察到两个公式都只包含正的关系原子，不存在相互否定的语句。因此无法进一步归结下去。

因此原命题不成立。

### (g)

证明：$(A) \Rightarrow (B)$，采用反证法有：

- 假设$(A)$为真，因此$\forall x \exists y (x \geq y)$，目标$(B)$为假，因此有$\lnot \forall y \exists x (x \geq y)$。

- 转化为CNF有：
  $$
  (\forall x \exists y (x \geq y)) \land \lnot(\forall y \exists (x \geq y))
  $$

- 进行化简：
  $$
  \begin{aligned}
  (\forall x \exists y (x \geq y)) \land \lnot(\forall y \exists x (x \geq y)) &\Rightarrow (\forall x \exists y (x \geq y)) \land (\exists y \lnot \exists x(x \geq y))\\
  &\Rightarrow (\forall x \exists y (x \geq y)) \land (\exists y \forall x (y > x))\\
  &\Rightarrow (\forall x \exists y (x \geq y)) \land (\exists x \forall y (x > y))
  \end{aligned}
  $$

- 观察到两个公式都只包含正的关系原子，不存在相互否定的语句。因此无法进一步归结下去。

因此原命题不成立。

## 题目四

## (1)

谓词：

`IsAmbulance(X)`：$x$是救护车

`IsAtInter(X)`：$x$在十字路口旁

`IsInInter(X)`：$x$在十字路口中

`IsAt(x, loc)`：$x$在$loc$

停车规则：

`Stop(X)`: 

## (2)

## (3)

## (4)

## (5)

## (6)

